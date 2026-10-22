import * as T from 'three';
import type { DicePresentation } from './dice-presentation';
import { dieGeometry,dieFaces,faceOrientation,settledOrientation } from './dice-geometry';
export const brassTheme={body:0x343b30,edge:0xb79c60,ink:'#e9ddbd',face:'#30382c'};
export type DiceTrayRenderer={show:(model:DicePresentation,instant:boolean)=>void;skip:()=>void;dispose:()=>void};
/** Lazy browser-only renderer. Its only input is an already completed presentation model. */
export function createDiceRenderer(host:HTMLElement,onFailure:()=>void,onSettle:()=>void):DiceTrayRenderer {
 const renderer=new T.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});
 renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.5));
 host.appendChild(renderer.domElement);renderer.domElement.setAttribute('aria-hidden','true');
 const scene=new T.Scene(),camera=new T.OrthographicCamera(-5,5,3,-3,.1,100);camera.position.z=15;
 scene.add(new T.HemisphereLight(0xffefd0,0x18221c,2.5));const key=new T.DirectionalLight(0xffdba0,3);key.position.set(-3,5,8);scene.add(key);
 const group=new T.Group();scene.add(group);
 const geometries=new Map<number,T.BufferGeometry>(),textures=new Map<string,T.CanvasTexture>();
 const owned:T.Material[]=[];let frame=0,started=0,disposed=false,settled=true;
 let dice:{group:T.Group;end:T.Quaternion;x:number;y:number;index:number}[]=[];
 function geometry(sides:number){let g=geometries.get(sides);if(!g){g=dieGeometry(sides);geometries.set(sides,g);}return g;}
 function texture(value:number){const id=String(value);let t=textures.get(id);if(t)return t;
  const c=document.createElement('canvas');c.width=c.height=128;const ctx=c.getContext('2d');if(!ctx)throw Error('Canvas unavailable');
  ctx.fillStyle=brassTheme.face;ctx.fillRect(0,0,128,128);ctx.fillStyle=brassTheme.ink;ctx.font='bold 88px Georgia';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(id,64,65);if(value===6||value===9){ctx.fillRect(46,110,36,3);}
  t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;textures.set(id,t);return t;
 }
 function draw(){if(disposed)return;try{renderer.render(scene,camera);}catch{onFailure();}}
 function size(){const width=Math.max(host.clientWidth,240),height=Math.max(host.clientHeight,240);renderer.setSize(width,height);const columns=Math.min(dice.length,width<500?3:5)||1;const rows=Math.ceil(dice.length/columns)||1;const halfHeight=Math.max(2,rows*1.3,columns*1.3/(width/height));camera.left=-halfHeight*width/height;camera.right=-camera.left;camera.top=halfHeight;camera.bottom=-halfHeight;camera.updateProjectionMatrix();dice.forEach((d,i)=>{d.x=(i%columns-(columns-1)/2)*2.5;d.y=((rows-1)/2-Math.floor(i/columns))*2.5;if(settled)d.group.position.set(d.x,d.y,0);});draw();}
 const observer=new ResizeObserver(size);observer.observe(host);
 function finish(){cancelAnimationFrame(frame);settled=true;for(const d of dice){d.group.position.set(d.x,d.y,0);d.group.quaternion.copy(d.end);}draw();onSettle();}
 function tick(now:number){if(disposed)return;const t=Math.min((now-started)/1150,1),ease=1-Math.pow(1-t,3);
  for(const d of dice){d.group.position.set(d.x+(1-ease)*(d.index%2?2:-2),d.y+Math.sin(t*Math.PI)*1.3,0);const spin=new T.Quaternion().setFromEuler(new T.Euler((1-ease)*Math.PI*4,(1-ease)*Math.PI*3,(1-ease)*.6));d.group.quaternion.copy(d.end).multiply(spin);}
  draw();if(t<1)frame=requestAnimationFrame(tick);else finish();
 }
 function clear(){cancelAnimationFrame(frame);group.traverse(o=>{if(o instanceof T.Mesh&&!Array.from(geometries.values()).includes(o.geometry))o.geometry.dispose();});group.clear();for(const m of owned)m.dispose();owned.length=0;dice=[];}
 const lost=(event:Event)=>{event.preventDefault();cancelAnimationFrame(frame);onFailure();};renderer.domElement.addEventListener('webglcontextlost',lost);
 return {
  show(model,instant){clear();settled=instant;
   // Large pools remain fully textual; never crowd or silently omit a die from a rendered pool.
   if(model.dice.length>20||model.dice.some(d=>![4,6,8,10,12,20].includes(d.sides)))throw Error('Use textual pool presentation');
   model.dice.forEach((die,index)=>{
    const g=geometry(die.sides),body=new T.Group(),material=new T.MeshStandardMaterial({color:brassTheme.body,roughness:.65,metalness:.35,transparent:die.discarded,opacity:die.discarded?.45:1});owned.push(material);body.add(new T.Mesh(g,material));
    dieFaces(g).forEach((face,i)=>{const mat=new T.MeshBasicMaterial({map:texture(i+1),transparent:die.discarded,opacity:die.discarded?.45:1,polygonOffset:true,polygonOffsetFactor:-1});owned.push(mat);const labelGeometry=new T.PlaneGeometry(die.sides===20?.4:die.sides===4?.55:.53,die.sides===20?.4:die.sides===4?.55:.53);const label=new T.Mesh(labelGeometry,mat);label.position.copy(face.center).addScaledVector(face.normal,.008);label.quaternion.copy(faceOrientation(face.normal));body.add(label);});
    group.add(body);dice.push({group:body,end:settledOrientation(g,die.value),x:0,y:0,index});
   });size();if(instant)finish();else{started=performance.now();frame=requestAnimationFrame(tick);}
  },skip:finish,
  dispose(){disposed=true;cancelAnimationFrame(frame);observer.disconnect();renderer.domElement.removeEventListener('webglcontextlost',lost);clear();for(const g of geometries.values())g.dispose();for(const t of textures.values())t.dispose();renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();}
 };
}
