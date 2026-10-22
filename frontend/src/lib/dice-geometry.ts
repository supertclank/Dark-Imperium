import * as T from 'three';
/** Geometry and face orientation are purely visual. Face numbers never resolve a roll. */
export function dieGeometry(sides:number):T.BufferGeometry {
 switch(sides){
 case 4:return new T.TetrahedronGeometry(1);
 case 6:return new T.BoxGeometry(1.35,1.35,1.35).toNonIndexed();
 case 8:return new T.OctahedronGeometry(1);
 case 12:return new T.DodecahedronGeometry(1);
 case 20:return new T.IcosahedronGeometry(1);
 case 10:{ // Ten-face pentagonal bipyramid, a deliberately stylised d10.
  const vertices=[0,0,1.15,0,0,-1.15];
  for(let i=0;i<5;i++)vertices.push(Math.cos(i*Math.PI*2/5),Math.sin(i*Math.PI*2/5),0);
  const indices:number[]=[];
  for(let i=0;i<5;i++){const a=2+i,b=2+(i+1)%5;indices.push(0,a,b,1,b,a);}
  return new T.PolyhedronGeometry(vertices,indices,1,0);
 }
 default:throw new Error('Unsupported presentation die');
 }
}
export function dieFaces(geometry:T.BufferGeometry){
 const p=geometry.getAttribute('position');
 const faces:{normal:T.Vector3;center:T.Vector3;vertices:T.Vector3[]}[]=[];
 for(let i=0;i<p.count;i+=3){
  const a=new T.Vector3().fromBufferAttribute(p,i),b=new T.Vector3().fromBufferAttribute(p,i+1),c=new T.Vector3().fromBufferAttribute(p,i+2);
  const normal=b.clone().sub(a).cross(c.clone().sub(a)).normalize();
  let face=faces.find(f=>f.normal.dot(normal)>.99999);
  if(!face){face={normal,center:new T.Vector3(),vertices:[]};faces.push(face);}
  for(const v of [a,b,c])if(!face.vertices.some(x=>x.distanceToSquared(v)<.000001))face.vertices.push(v);
 }
 for(const face of faces){for(const v of face.vertices)face.center.add(v);face.center.divideScalar(face.vertices.length);}
 return faces;
}
export function faceOrientation(normal:T.Vector3){return new T.Quaternion().setFromUnitVectors(new T.Vector3(0,0,1),normal);}
export function settledOrientation(geometry:T.BufferGeometry,value:number){
 const face=dieFaces(geometry)[value-1];if(!face)throw new Error('Invalid supplied face');
 // Invert the numeral's local basis so the supplied face is dominantly front-facing with a small tilt that reveals depth.
 return new T.Quaternion().setFromEuler(new T.Euler(.18,-.22,0)).multiply(faceOrientation(face.normal).invert());
}

