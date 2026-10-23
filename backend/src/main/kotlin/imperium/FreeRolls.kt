package imperium

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.sql.Connection
import java.util.UUID
import java.time.Instant

@Serializable data class FreeDiePool(val count:Int,val sides:Int)
@Serializable data class FreeRollRequest(val requestId:String,val pool:List<FreeDiePool>)
/** Authenticated raw pools. No character, modifier, keep rule, or client result accepted. */
class FreeRolls(private val db:Database,private val dice:DiceEngine=DiceEngine()) {
 fun execute(owner:UUID,request:FreeRollRequest,rawValues:List<List<Int>>?=null,validateOnly:Boolean=false,sessionCon:Connection?=null):JsonObject {
  val id=try{UUID.fromString(request.requestId)}catch(_:IllegalArgumentException){throw ApiException(422,"INVALID_POOL","A request UUID is required.")}
  if(request.pool.isEmpty() || request.pool.size>7 || request.pool.any{it.count !in 1..100 || it.sides !in setOf(4,6,8,10,12,20,100)} || request.pool.sumOf{it.count.toLong()} !in 1L..100L || request.pool.map{it.sides}.distinct().size!=request.pool.size)
   throw ApiException(422,"INVALID_POOL","Choose 1–100 dice, with one group per supported die type.")
  val digest=sha(canonicalJson(Json.encodeToJsonElement(FreeRollRequest.serializer(),request)))
  val operation:(Connection)->JsonObject=operation@{con->
   con.query("SELECT pg_advisory_xact_lock(hashtextextended(?,0))","free:$owner:$id"){0}
   if(sessionCon==null&&con.query("SELECT id FROM physical_roll_sessions WHERE user_id=? AND request_id=?",owner,id){it.getString(1)}.isNotEmpty())throw ApiException(409,"SESSION_REQUIRED","Complete this request through its authorised roll session.")
   val old=con.query("SELECT request_digest,result FROM free_rolls WHERE user_id=? AND request_id=?",owner,id){it.getString(1) to Json.parseToJsonElement(it.getString(2)).jsonObject}.singleOrNull()
   if(old!=null){if(old.first!=digest)throw ApiException(409,"IDEMPOTENCY_CONFLICT","Request ID was already used for a different pool.");return@operation old.second}
   val groups=request.pool.map{DiceGroup(it.count,it.sides)}
   if(validateOnly)return@operation obj("groups" to groups.map{obj("count" to it.count,"sides" to it.sides,"keep" to it.keep.name,"keepCount" to it.keepCount)},"modifier" to 0,"label" to request.pool.joinToString(" + "){"${it.count}d${it.sides}"})
   val resolved=if(rawValues==null)dice.resolve(groups,0)else dice.resolveRaw(groups,0,rawValues)
   val resultId=UUID.randomUUID();val now=Instant.now()
   val definition=obj("category" to "FREE_ROLL","groups" to request.pool.map{obj("count" to it.count,"sides" to it.sides)},"modifier" to 0,"authority" to "SERVER")
   val result=obj("id" to resultId.toString(),"requestId" to id.toString(),"characterId" to "","characterName" to "Free dice","label" to request.pool.joinToString(" + "){"${it.count}d${it.sides}"},"rollType" to "FREE_ROLL",
    "requestedRollId" to "FREE_ROLL","rulesetProfileId" to "","rulesetDigest" to "","actionId" to null,"definition" to definition,
    "timestamp" to now.toString(),"total" to resolved.total,"dice" to Json.encodeToJsonElement(DiceResolution.serializer(),resolved),
    "naturalResult" to null,"naturalOne" to false,"criticalCandidate" to false,"damageType" to null,"parentResultId" to null,
    "context" to obj("ability" to null,"targetResolution" to "MANUAL","criticalDamage" to "NOT_APPLIED"),"visibility" to "PRIVATE",
    "stateVersionBefore" to 0,"stateVersionAfter" to 0,"consumption" to null,"grenade" to null)
   con.execute("INSERT INTO free_rolls(id,user_id,request_id,request_digest,result,created_at) VALUES (?,?,?,?,?::jsonb,?)",resultId,owner,id,digest,result.toString(),java.sql.Timestamp.from(now))
   result
  }
  return if(sessionCon!=null)operation(sessionCon)else db.transaction(operation)
 }
 fun history(owner:UUID):JsonObject=db.read{con->
  val rows=con.query("SELECT result FROM free_rolls WHERE user_id=? ORDER BY created_at DESC,id DESC LIMIT 26",owner){Json.parseToJsonElement(it.getString(1)).jsonObject}
  obj("items" to rows.take(25),"limit" to 25,"hasMore" to (rows.size>25))
 }
}
