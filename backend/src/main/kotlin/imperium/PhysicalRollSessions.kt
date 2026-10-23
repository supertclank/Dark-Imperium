package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.security.SecureRandom
import java.sql.Connection
import java.time.Instant
import java.util.UUID

@Serializable data class PhysicalSubmission(val values:List<List<Int>>?=null,val fallback:Boolean=false,val physicsVersion:String="rapier-0.21.0-di-1",val geometryVersion:String="di-physical-2")
class PhysicalRollSessions(private val db:Database,private val characters:CharacterRolls,private val free:FreeRolls) {
 private val random=SecureRandom()
 private fun fail(code:String,message:String,status:Int=422):Nothing=throw ApiException(status,code,message)
 fun character(owner:UUID,id:UUID,request:RollRequest)=create(owner,id,request.requestId,Json.encodeToJsonElement(RollRequest.serializer(),request).jsonObject)
 fun free(owner:UUID,request:FreeRollRequest)=create(owner,null,request.requestId,Json.encodeToJsonElement(FreeRollRequest.serializer(),request).jsonObject)
 private fun view(row:JsonObject):JsonObject {
  val spec=row.getValue("specification").jsonObject
  return obj("rollSessionId" to row.text("id"),"label" to spec.text("label"),"groups" to spec.arr("groups"),"modifier" to spec.num("modifier"),"presentationSeed" to row.text("presentationSeed"),"expiresAt" to row.text("expiresAt"),"status" to if(row.text("status")=="CREATED"&&Instant.parse(row.text("expiresAt")).isBefore(Instant.now()))"EXPIRED" else row.text("status"),"physicsVersion" to "rapier-0.21.0-di-1","geometryVersion" to "di-physical-2","maxRerolls" to 3,"result" to row["result"])
 }
 private fun load(con:Connection,owner:UUID,id:UUID,lock:Boolean=true):JsonObject=con.query("SELECT id,character_id,request,specification,presentation_seed,expires_at,status,submission_digest,result FROM physical_roll_sessions WHERE id=? AND user_id=?"+if(lock)" FOR UPDATE" else "",id,owner){r->obj("id" to r.getString(1),"characterId" to r.getString(2),"request" to Json.parseToJsonElement(r.getString(3)),"specification" to Json.parseToJsonElement(r.getString(4)),"presentationSeed" to r.getString(5),"expiresAt" to r.getTimestamp(6).toInstant().toString(),"status" to r.getString(7),"submissionDigest" to r.getString(8),"result" to r.getString(9)?.let{Json.parseToJsonElement(it)})}.singleOrNull()?:fail("SESSION_NOT_FOUND","Roll session not found.",404)
 private fun create(owner:UUID,character:UUID?,requestId:String,request:JsonObject):JsonObject=db.transaction{con->
  val requestUuid=uuid(requestId);val digest=sha(canonicalJson(obj("character" to character?.toString(),"request" to request)))
  con.query("SELECT pg_advisory_xact_lock(hashtextextended(?,0))","session:$owner:$requestUuid"){0}
  val old=con.query("SELECT id,request_digest FROM physical_roll_sessions WHERE user_id=? AND request_id=?",owner,requestUuid){it.getObject(1,UUID::class.java) to it.getString(2)}.singleOrNull()
  if(old!=null){if(old.second!=digest)fail("IDEMPOTENCY_CONFLICT","Request ID already used for different choices.",409);return@transaction view(load(con,owner,old.first))}
  val spec=if(character!=null)characters.execute(owner,character,Json.decodeFromJsonElement(RollRequest.serializer(),request),validateOnly=true,sessionCon=con)else free.execute(owner,Json.decodeFromJsonElement(FreeRollRequest.serializer(),request),validateOnly=true,sessionCon=con)
  if(!spec.containsKey("groups"))fail("IDEMPOTENCY_CONFLICT","This request already produced a legacy result. Use a new request ID.",409)
  val item=spec["reservedItem"]?.jsonPrimitive?.contentOrNull
  if(item!=null){val count=con.query("SELECT count(*) FROM physical_roll_sessions WHERE character_id=? AND reserved_item=? AND status='CREATED' AND expires_at>now()",character,item){it.getInt(1)}.single();if(count>=spec.num("quantity"))fail("RESOURCE_RESERVED","All remaining items are reserved by active rolls.",409)}
  val id=UUID.randomUUID();val seed=ByteArray(32).also{random.nextBytes(it)}.joinToString(""){"%02x".format(it)}
  con.execute("INSERT INTO physical_roll_sessions(id,user_id,character_id,request_id,request_digest,request,specification,presentation_seed,reserved_item,expires_at) VALUES (?,?,?,?,?,?::jsonb,?::jsonb,?,?,?)",id,owner,character,requestUuid,digest,request.toString(),spec.toString(),seed,item,java.sql.Timestamp.from(Instant.now().plusSeconds(300)))
  view(load(con,owner,id))
 }
 fun finalize(owner:UUID,id:UUID,input:PhysicalSubmission):JsonObject=db.transaction{con->
  val row=load(con,owner,id);val digest=sha(canonicalJson(Json.encodeToJsonElement(PhysicalSubmission.serializer(),input)))
  if(row.text("status")=="COMPLETED"){if(row["submissionDigest"]?.jsonPrimitive?.content!=digest)fail("IDEMPOTENCY_CONFLICT","This roll was completed with a different submission.",409);return@transaction row.getValue("result").jsonObject}
  if(row.text("status")!="CREATED")fail("SESSION_CLOSED","This roll was cancelled.",409)
  if(!Instant.parse(row.text("expiresAt")).isAfter(Instant.now()))fail("SESSION_EXPIRED","The roll expired; no item was consumed.",409)
  if(input.physicsVersion!="rapier-0.21.0-di-1"||input.geometryVersion!="di-physical-2")fail("PHYSICS_VERSION","Unsupported physics or geometry version.")
  val groups=row.getValue("specification").jsonObject.objects("groups")
  if(input.fallback){if(input.values!=null)fail("INVALID_VALUES","Fallback cannot include client values.")}
  else {val values=input.values?:fail("INVALID_VALUES","Physical values are required.");if(values.size!=groups.size||groups.indices.any{i->values[i].size!=groups[i].num("count")||values[i].any{it !in 1..groups[i].num("sides")}})fail("INVALID_VALUES","Submit exactly the authorised dice counts and ranges.")}
  val request=row.getValue("request").jsonObject;val character=row["characterId"]?.jsonPrimitive?.contentOrNull
  val result=if(character!=null)characters.execute(owner,uuid(character),Json.decodeFromJsonElement(RollRequest.serializer(),request),input.values,sessionCon=con,reservationSession=id)else free.execute(owner,Json.decodeFromJsonElement(FreeRollRequest.serializer(),request),input.values,sessionCon=con)
  val enriched=JsonObject(result+mapOf("physical" to obj("rollSessionId" to id.toString(),"source" to if(input.fallback)"SERVER_FALLBACK" else "PHYSICS","physicsVersion" to input.physicsVersion,"geometryVersion" to input.geometryVersion,"presentationSeed" to row.text("presentationSeed"),"rawPhysicalValues" to input.values)))
  val table=if(character!=null)"character_rolls" else "free_rolls"
  con.execute("UPDATE $table SET result=?::jsonb WHERE id=?",enriched.toString(),uuid(result.text("id")))
  con.execute("UPDATE physical_roll_sessions SET status='COMPLETED',submission_digest=?,result=?::jsonb WHERE id=?",digest,enriched.toString(),id)
  enriched
 }
 fun cancel(owner:UUID,id:UUID):JsonObject=db.transaction{con->val row=load(con,owner,id);if(row.text("status")=="COMPLETED")fail("SESSION_CLOSED","Completed rolls cannot be cancelled.",409);con.execute("UPDATE physical_roll_sessions SET status='CANCELLED' WHERE id=?",id);obj("status" to "CANCELLED")}
}
