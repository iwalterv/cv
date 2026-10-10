#version 300 es
precision highp float;
uniform vec2 uRes;
uniform int uType;      // 0 anillo, 1 argolla, 2 colgante, 3 aretes, 4 pulsera, 5 reloj, 6 jade tallado
uniform int uGem;       // 0 nada, 1 brillante, 2 oval facetado, 3 talla esmeralda, 4 perla, 5 jade, 6 cabujón
uniform vec3 uMetal;    // F0 del metal
uniform vec3 uGemCol;   // color de la piedra / esfera
uniform vec3 uCam;      // yaw, pitch, distancia
uniform vec3 uTarget;
uniform int uQ;         // 1 = calidad de estudio, 0 = vista en vivo
uniform float uSeed;
out vec4 fragColor;

#define PI 3.14159265
int T; int GK;
float YAW; vec3 BC; float BR;
bool noGlass = false;

mat2 rot(float a){ float c=cos(a), s=sin(a); return mat2(c,-s,s,c); }
float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))+uSeed)*43758.5453); }
float sdBox(vec3 p, vec3 b){ vec3 q=abs(p)-b; return length(max(q,0.))+min(max(q.x,max(q.y,q.z)),0.); }
float sdCap(vec3 p, vec3 a, vec3 b, float r){ vec3 pa=p-a, ba=b-a; float h=clamp(dot(pa,ba)/dot(ba,ba),0.,1.); return length(pa-ba*h)-r; }
float sdTorus(vec3 p, vec2 t){ vec2 q=vec2(length(p.xz)-t.x,p.y); return length(q)-t.y; }
float sdCylZ(vec3 p, float r, float h, float rr){ vec2 d=abs(vec2(length(p.xy),p.z))-vec2(r-rr,h-rr); return min(max(d.x,d.y),0.)+length(max(d,0.))-rr; }
float sdEll(vec3 p, vec3 r){ float k0=length(p/r); float k1=length(p/(r*r)); return k0*(k0-1.)/k1; }
float smin(float a, float b, float k){ float h=clamp(.5+.5*(b-a)/k,0.,1.); return mix(b,a,h)-k*h*(1.-h); }
float sdBand(vec3 p, float R, vec2 hw, float rr){ vec2 q=vec2(length(p.xy)-R, p.z); vec2 d=abs(q)-(hw-rr); return length(max(d,0.))+min(max(d.x,d.y),0.)-rr; }

float sdBrilliant(vec3 p, float r){
  float l=length(p.xz);
  float sec=2.*PI/8.;
  float a=atan(p.z,p.x);
  a=mod(a+sec*.5,sec)-sec*.5;
  vec3 q=vec3(l*cos(a), p.y, abs(l*sin(a)));
  float d=p.y-0.36*r;
  d=max(d, l-r);
  d=max(d, dot(q-vec3(r,0.03*r,0.), normalize(vec3(0.66,1.,0.))));
  d=max(d, dot(q-vec3(r,-0.03*r,0.), normalize(vec3(0.86,-1.,0.))));
  float h=sec*.5;
  vec3 q2=vec3(q.x*cos(h)+q.z*sin(h), q.y, 0.);
  d=max(d, dot(q2-vec3(r*0.985,0.07*r,0.), normalize(vec3(0.48,1.,0.))));
  d=max(d, dot(q2-vec3(r*0.99,-0.06*r,0.), normalize(vec3(1.05,-1.,0.))));
  return d;
}
float sdEmeraldCut(vec3 p, vec2 s){
  vec3 a=abs(p);
  float d=max(a.x-s.x, a.z-s.y);
  d=max(d, (a.x+a.z-(s.x+s.y)+0.09)*0.7071);
  d=max(d, p.y-0.10);
  d=max(d, -p.y-0.24);
  d=max(d, (a.x-s.x+(p.y-0.01)*0.95)*0.72);
  d=max(d, (a.z-s.y+(p.y-0.01)*0.95)*0.72);
  d=max(d, (a.x-s.x+(p.y-0.06)*0.45)*0.9);
  d=max(d, (a.z-s.y+(p.y-0.06)*0.45)*0.9);
  d=max(d, (a.x-s.x-(p.y+0.01)*0.80)*0.78);
  d=max(d, (a.z-s.y-(p.y+0.01)*0.80)*0.78);
  return d;
}

/* ---------- geometría compartida ---------- */
const float RR=0.9;
vec3 ringGemC(){ return vec3(0., 2.*RR+0.16+0.30, 0.); }
vec3 pendC(){ return vec3(0., 1.55, 0.); }

// piedra en coordenadas locales (eje y = mesa)
float gemLocal(vec3 q){
  if(GK==1) return sdBrilliant(q, 0.36);
  if(GK==2) return sdBrilliant(vec3(q.x, q.y, q.z/1.3), 0.30)*0.85;
  if(GK==3) return sdEmeraldCut(q, vec2(0.25,0.34));
  return 1e9;
}
// piedras transparentes de la escena
float gemD(vec3 p){
  if(GK<1||GK>3) return 1e9;
  if(T==0){ return gemLocal(p-ringGemC()); }
  if(T==2||T==3){
    vec3 q=p-pendC();
    if(T==3){ q=p-vec3(0.,1.25,0.); q.x=abs(q.x)-0.62; }
    vec3 l=vec3(q.x, q.z, -q.y);           // la mesa mira a la cámara
    l.z/=1.35; return gemLocal(l*1.0)*0.8;
  }
  if(T==4){
    vec3 q=p-vec3(0.,0.16,0.);
    float n=28., sec=2.*PI/n;
    float a=atan(q.z,q.x); a=mod(a+sec*.5,sec)-sec*.5;
    float l=length(q.xz);
    vec3 s=vec3(l*cos(a)-1.25, q.y-0.06, l*sin(a));
    return sdBrilliant(s, 0.115);
  }
  return 1e9;
}

/* ---------- cadenas ---------- */
float link(vec3 q, float R, float e, float r){ vec2 a=vec2(max(abs(q.x)-e,0.), q.y); return length(vec2(length(a)-R, q.z))-r; }
float sdChain(vec3 p, vec3 a, vec3 b){
  vec3 ba=b-a; float L=length(ba); vec3 t=ba/L;
  vec3 nr=normalize(cross(t, vec3(0.,0.,1.))); vec3 bn=cross(t,nr);
  vec3 pa=p-a; float x=dot(pa,t), y=dot(pa,nr), z=dot(pa,bn);
  if(x<-0.2||x>L+0.2) return max(abs(x-L*.5)-L*.5, length(vec2(y,z)))-0.02;
  float s=0.105, N=floor(L/s);
  float x1=x-s*clamp(round(x/s),0.,N);
  float x2=x-s*.5-s*clamp(round((x-s*.5)/s),0.,N-1.);
  return min(link(vec3(x1,y,z),0.034,0.026,0.0115), link(vec3(x2,z,y),0.034,0.026,0.0115));
}


/* ---------- cadena cubana ---------- */
float cubanLink(vec3 s, float sg){
  s.xz=rot(sg*0.42)*s.xz;
  s.xy=rot(sg*0.38)*s.xy;
  float e=0.09, R=0.13;
  vec2 w=vec2(length(vec2(s.x, max(abs(s.z)-e,0.)))-R, s.y);
  float d=(length(w*vec2(1.,1.25))-0.058)/1.25;
  d=max(d, abs(s.y)-0.05);
  return d*0.9;
}
float sdCuban(vec3 p){
  vec3 q=p-vec3(0.,0.09,0.);
  float n=26., sec=2.*PI/n, Rc=1.45;
  float a=atan(q.z,q.x), l=length(q.xz);
  float d=1e9;
  for(int k=-1;k<=1;k++){
    float a1=mod(a+sec*.5,sec)-sec*.5+float(k)*sec;
    d=min(d, cubanLink(vec3(l*cos(a1)-Rc, q.y, l*sin(a1)), 1.));
    float a2=mod(a,sec)-sec*.5+float(k)*sec;
    d=min(d, cubanLink(vec3(l*cos(a2)-Rc, q.y, l*sin(a2)), -1.));
  }
  float ca=1.9; vec2 cs=vec2(cos(ca),sin(ca));
  vec3 c=vec3(q.x*cs.x+q.z*cs.y-Rc, q.y, -q.x*cs.y+q.z*cs.x);
  float clasp=sdBox(c, vec3(0.15,0.06,0.30))-0.02;
  return min(d, clasp);
}

/* ---------- escena: devuelve (distancia, material) ----------
   1 metal · 2 piedra · 3 perla · 4 jade · 5 esfera · 6 piel · 7 cristal · 8 cordón */
vec2 U(vec2 a, vec2 b){ return a.x<b.x?a:b; }

vec2 mapRing(vec3 p){
  bool plain = (T==1)||GK==0;
  float hw = plain ? 0.17 : 0.105;
  float th = plain ? 0.07 : 0.075;
  vec3 q=p-vec3(0.,RR+th,0.);
  float taper = plain ? 0. : smoothstep(0.2,1.0,q.y)*0.03;
  vec2 res=vec2(sdBand(q,RR,vec2(th,hw-taper),0.035),1.);
  if(plain) return res;
  vec3 gc=ringGemC();
  float top=2.*RR+2.*th;
  float m=1e9;
  m=min(m, sdCap(p, vec3(-0.34,top-0.06,0.), gc+vec3(-0.15,-0.19,0.), 0.05));
  m=min(m, sdCap(p, vec3( 0.34,top-0.06,0.), gc+vec3( 0.15,-0.19,0.), 0.05));
  if(GK<=3){
    m=min(m, sdTorus(p-(gc-vec3(0.,0.20,0.)), vec2(0.19,0.028)));
    for(int i=0;i<4;i++){
      float a=PI*.25+float(i)*PI*.5;
      vec2 cs=vec2(cos(a),sin(a));
      vec3 tip, base;
      if(GK==3){ tip=vec3(sign(cs.x)*0.21, gc.y+0.05, sign(cs.y)*0.30); base=vec3(sign(cs.x)*0.13, gc.y-0.26, sign(cs.y)*0.13); }
      else { float rr=(GK==2)?0.29:0.345; tip=vec3(cs.x*rr*(GK==2?1.0:1.0), gc.y+0.055, cs.y*rr*(GK==2?1.3:1.0)); base=vec3(cs.x*0.16, gc.y-0.28, cs.y*0.16); }
      m=min(m, sdCap(p, base, tip, 0.03));
    }
  } else {
    float cup=sdEll(p-(gc-vec3(0.,0.12,0.)), vec3(0.34,0.16,0.30));
    cup=max(cup, p.y-(gc.y-0.06));
    m=min(m, cup);
  }
  res=U(res, vec2(smin(m, res.x, 0.03),1.));
  if(GK<=3) res=U(res, vec2(gemD(p),2.));
  else if(GK==4) res=U(res, vec2(length(p-(gc+vec3(0.,0.04,0.)))-0.30,3.));
  else res=U(res, vec2(sdEll(p-(gc-vec3(0.,0.04,0.)), vec3(0.30,0.20,0.26)), GK==5?4.:2.));
  return res;
}

vec2 mapDrop(vec3 q){ // un colgante o arete centrado en q
  vec2 res=vec2(1e9,0.);
  if(GK>=1&&GK<=3){
    vec3 l=vec3(q.x,q.z,-q.y); l.z/=1.35;
    float rim=sdTorus(vec3(l.x, l.y+0.01, l.z), vec2(0.33,0.035));
    res=vec2(rim*0.8,1.);
    res=U(res, vec2(sdCap(q, vec3(0.,0.42,0.), vec3(0.,0.50,0.), 0.035),1.));
  } else if(GK==0){
    res=vec2(sdEll(q, vec3(0.24,0.34,0.05)),1.);
    res=U(res, vec2(sdCap(q, vec3(0.,0.34,0.), vec3(0.,0.47,0.), 0.035),1.));
  } else if(GK==4){
    res=vec2(length(q)-0.30,3.);
    res=U(res, vec2(sdEll(q-vec3(0.,0.28,0.), vec3(0.09,0.06,0.09)),1.));
  } else {
    res=vec2(sdEll(q, vec3(0.30,0.40,0.12)), GK==5?4.:2.);
    res=U(res, vec2(sdCap(q, vec3(0.,0.38,0.), vec3(0.,0.47,0.), 0.04),1.));
  }
  return res;
}

vec2 map(vec3 p){
  vec2 res=vec2(1e9,0.);
  if(T==0||T==1){ res=mapRing(p); }
  else if(T==2){
    vec3 c=pendC();
    res=mapDrop(p-c);
    if(GK>=1&&GK<=3) res=U(res, vec2(gemD(p),2.));
    vec3 bail=c+vec3(0.,0.56,0.);
    res=U(res, vec2(sdTorus((p-bail).xzy, vec2(0.07,0.022)),1.));
    res=U(res, vec2(sdChain(p, bail+vec3(-0.03,0.06,0.), bail+vec3(-1.7,2.6,-0.2)),1.));
    res=U(res, vec2(sdChain(p, bail+vec3( 0.03,0.06,0.), bail+vec3( 1.7,2.6,-0.2)),1.));
  }
  else if(T==3){
    vec3 q=p-vec3(0.,1.25,0.); q.x=abs(q.x)-0.62;
    res=mapDrop(q);
    if(GK<=3) res=U(res, vec2(gemD(p),2.));
    vec3 h=q-vec3(0.,0.62,0.);
    vec3 hh=h-vec3(0.13,0.10,0.);
    float arc=length(vec2(abs(length(hh.xy)-0.13), hh.z))-0.017; arc=max(arc,-hh.y);
    arc=min(arc, sdCap(h, vec3(0.26,0.10,0.), vec3(0.26,-0.06,0.), 0.017));
    float stem=sdCap(h, vec3(0.,-0.12,0.), vec3(0.,0.10,0.), 0.017);
    res=U(res, vec2(min(stem, arc),1.));
    res=U(res, vec2(sdEll(h-vec3(0.,-0.14,0.), vec3(0.07,0.05,0.07)),1.));
  }
  else if(T==4){
    if(GK==5){
      vec3 q=p-vec3(0.,0.17,0.);
      float n=20., sec=2.*PI/n;
      float a=atan(q.z,q.x); a=mod(a+sec*.5,sec)-sec*.5; float l=length(q.xz);
      vec3 s=vec3(l*cos(a)-1.15, q.y, l*sin(a));
      res=vec2(length(s)-0.17,4.);
      res=U(res, vec2(length(vec2(l-1.15,q.y))-0.012,8.));
      res=U(res, vec2(sdEll(p-vec3(1.15,0.17,0.), vec3(0.08,0.12,0.12)),1.));
    } else if(GK==0){
      vec3 q=p-vec3(0.,1.15,0.);
      res=vec2(sdBand(q,1.05,vec2(0.075,0.16),0.06),1.);
    } else {
      vec3 q=p-vec3(0.,0.16,0.);
      float l=length(q.xz);
      float band=length(max(abs(vec2(l-1.25, q.y+0.02))-vec2(0.07,0.05),0.))-0.025;
      float n=28., sec=2.*PI/n;
      float a=atan(q.z,q.x); a=mod(a+sec*.5,sec)-sec*.5;
      vec3 s=vec3(l*cos(a)-1.25, q.y, l*sin(a));
      float cup=sdTorus(s-vec3(0.,0.03,0.), vec2(0.105,0.022));
      res=vec2(min(band,cup),1.);
      res=U(res, vec2(gemD(p),2.));
    }
  }
  else if(T==5){
    vec3 c=vec3(0.,1.07,0.);
    vec3 q=p-c;
    // correa: lazo en el plano yz
    vec3 s=q-vec3(0.,0.,-0.98);
    float sr=length(s.yz)-0.98;
    float strap=length(max(abs(vec2(sr, s.x))-vec2(0.03,0.30),0.))-0.02;
    
    res=vec2(strap, (uMetal.r<0.7&&uMetal.g<0.7) ? 1. : 6.);
    float cse=sdCylZ(q-vec3(0.,0.,0.06), 0.58, 0.11, 0.05);
    vec3 lq=vec3(abs(q.x)-0.22, abs(q.y)-0.58, q.z-0.05); float lug=sdBox(lq, vec3(0.05,0.12,0.06))-0.02;
    float crown=sdCylZ((q-vec3(0.66,0.,0.06)).zyx, 0.07, 0.07, 0.02);
    float bez=sdTorus((q-vec3(0.,0.,0.215)).xzy, vec2(0.53,0.05));
    res=U(res, vec2(smin(cse,crown,0.01),1.));
    res=U(res, vec2(bez,1.));
    float dial=sdCylZ(q-vec3(0.,0.,0.19), 0.50, 0.02, 0.005);
    res=U(res, vec2(dial,5.));
    // índices
    float ang=atan(q.x,q.y); float sec=PI/6.; float aa=mod(ang+sec*.5,sec)-sec*.5;
    float lr=length(q.xy);
    vec3 iq=vec3(lr*sin(aa), lr*cos(aa)-0.40, q.z-0.215);
    float idx=sdBox(iq, vec3(0.012,0.055,0.008));
    // agujas
    vec3 hq=q-vec3(0.,0.,0.23);
    vec3 h1=hq; h1.xy=rot(-0.9)*h1.xy; float hand1=sdBox(h1-vec3(0.,0.13,0.), vec3(0.016,0.15,0.006));
    vec3 h2=hq; h2.xy=rot(2.25)*h2.xy; float hand2=sdBox(h2-vec3(0.,0.20,0.01), vec3(0.012,0.22,0.006));
    float pin=sdCylZ(hq, 0.025, 0.02, 0.005);
    res=U(res, vec2(min(min(idx,hand1),min(hand2,pin)),1.));
  }
  else if(T==7){
    res=vec2(sdCuban(p),1.);
  }
  else if(T==6){
    vec3 c=pendC()+vec3(0.,-0.1,0.);
    vec3 q=p-c;
    float d=sdEll(q, vec3(0.42,0.55,0.13));
    float groove=length(vec2(length(q.xy)-0.27, q.z-0.12))-0.035;
    float groove2=length(vec2(length(q.xy*vec2(1.,1.))-0.11, q.z-0.13))-0.03;
    d=max(d,-min(groove,groove2));
    res=vec2(d,4.);
    vec3 b=q-vec3(0.,0.62,0.);
    res=U(res, vec2(sdTorus(b.xzy, vec2(0.09,0.03)),1.));
    res=U(res, vec2(sdCap(p, c+vec3(0.,0.68,0.), c+vec3(-1.4,3.2,-0.2), 0.022),8.));
    res=U(res, vec2(sdCap(p, c+vec3(0.,0.68,0.), c+vec3( 1.4,3.2,-0.2), 0.022),8.));
  }
  return res;
}

vec3 calcN(vec3 p){
  vec2 e=vec2(1.,-1.)*0.0007;
  return normalize(e.xyy*map(p+e.xyy).x + e.yyx*map(p+e.yyx).x + e.yxy*map(p+e.yxy).x + e.xxx*map(p+e.xxx).x);
}
vec3 gemN(vec3 p){
  vec2 e=vec2(1.,-1.)*0.0006;
  return normalize(e.xyy*gemD(p+e.xyy) + e.yyx*gemD(p+e.yyx) + e.yxy*gemD(p+e.yxy) + e.xxx*gemD(p+e.xxx));
}

/* ---------- estudio de fotografía ---------- */
vec3 studio(vec3 d){ d.xz=rot(YAW)*d.xz; return d; }
vec3 env(vec3 dw){
  vec3 d=studio(dw);
  float az=atan(d.x,d.z), el=d.y;
  vec3 c=vec3(0.010,0.010,0.013)+vec3(0.035,0.034,0.04)*smoothstep(-0.1,1.,el);
  // caja de luz superior
  vec2 tp=d.xz/max(d.y,0.01);
  c+=vec3(3.4,3.3,3.1)*smoothstep(0.75,0.6,max(abs(tp.x)*0.9,abs(tp.y+0.15)))*step(0.,d.y);
  // tiras laterales
  c+=vec3(3.0,2.9,2.75)*smoothstep(0.10,0.05,abs(az+1.15))*smoothstep(-0.30,-0.10,el)*smoothstep(0.80,0.60,el);
  c+=vec3(2.4,2.55,2.9)*smoothstep(0.08,0.04,abs(az-1.30))*smoothstep(-0.25,-0.05,el)*smoothstep(0.75,0.55,el);
  // luz de contorno (fría) y tarjeta frontal
  c+=vec3(0.55,0.75,1.25)*smoothstep(0.45,0.25,abs(abs(az)-PI))*smoothstep(0.,0.15,el)*smoothstep(0.65,0.35,el);
  c+=vec3(1.1)*smoothstep(0.55,0.40,abs(az))*smoothstep(-0.55,-0.35,el)*smoothstep(0.10,-0.05,el);
  c+=vec3(0.9,0.75,0.55)*smoothstep(0.12,0.06,abs(az-0.55))*smoothstep(0.05,0.15,el)*smoothstep(0.45,0.3,el)*0.6;
  // anillo de pequeñas luces cenitales: chispas en las facetas
  float ra=mod(az+0.2,0.785)-0.39;
  c+=vec3(4.5)*smoothstep(0.07,0.03,abs(ra))*smoothstep(0.03,0.0,abs(el-0.72));
  c+=vec3(1.6,1.6,1.7)*smoothstep(0.35,0.2,abs(az+2.3))*smoothstep(0.25,0.4,el)*smoothstep(0.7,0.55,el);
  return c;
}
vec3 keyL(){ vec3 l=normalize(vec3(-0.55,0.85,0.45)); l.xz=rot(-YAW)*l.xz; return l; }

float fres(float c, float f0){ return f0+(1.-f0)*pow(1.-clamp(c,0.,1.),5.); }

float trace(vec3 ro, vec3 rd, float tmax, out float mat){
  mat=0.;
  vec3 oc=ro-BC; float bb=dot(oc,rd); float cc=dot(oc,oc)-BR*BR; float hh=bb*bb-cc;
  if(hh<0.) return -1.;
  hh=sqrt(hh); float t=max(-bb-hh,0.); tmax=min(tmax,-bb+hh);
  if(tmax<0.) return -1.;
  for(int i=0;i<180;i++){
    vec2 h=map(ro+rd*t);
    if(h.x<0.0004*t+0.0003){ mat=h.y; return t; }
    t+=h.x*0.9;
    if(t>tmax) break;
  }
  return -1.;
}
float softShadow(vec3 ro, vec3 rd){
  float r=1., t=0.02;
  vec3 oc=ro-BC; float bb=dot(oc,rd); float hh=bb*bb-(dot(oc,oc)-BR*BR); if(hh<0.) return 1.;
  for(int i=0;i<48;i++){ float h=map(ro+rd*t).x; r=min(r, 10.*h/t); t+=clamp(h,0.01,0.25); if(r<0.002||t>6.) break; }
  return clamp(r,0.,1.);
}
float ao(vec3 p, vec3 n){
  float o=0., s=1.;
  for(int i=1;i<=5;i++){ float h=0.03*float(i); o+=(h-map(p+n*h).x)*s; s*=0.7; }
  return clamp(1.-2.2*o,0.,1.);
}

vec3 metalCol(vec3 p, vec3 n, vec3 rd, bool deep){
  vec3 r=reflect(rd,n);
  vec3 c=vec3(0.);
  int ns = uQ==1 ? 6 : 2;
  for(int i=0;i<6;i++){ if(i>=ns) break;
    vec3 j=vec3(hash(p.xy*91.+float(i)), hash(p.yz*77.+float(i)*3.1), hash(p.zx*53.+float(i)*7.7))-.5;
    c+=env(normalize(r+j*0.07));
  }
  c/=float(ns);
  if(deep){
    float m; float t=trace(p+n*0.004, r, 4., m);
    if(t>0.){
      vec3 q=p+n*0.004+r*t; vec3 n2=calcN(q);
      vec3 base = m==2. ? uGemCol*0.6+env(reflect(r,n2))*0.3 : m==1. ? env(reflect(r,n2))*uMetal : (m==3.||m==4.)? uGemCol*0.5 : vec3(0.02);
      c=mix(c, base*0.85, 0.92);
    }
  }
  vec3 F=uMetal+(1.-uMetal)*pow(1.-max(dot(n,-rd),0.),5.);
  return c*F;
}

vec3 gemPass(vec3 p, vec3 n, vec3 rd, float ior, vec3 absorb){
  float ci=max(dot(-rd,n),0.);
  float F=fres(ci, pow((ior-1.)/(ior+1.),2.));
  vec3 col=env(reflect(rd,n))*F;
  vec3 d=refract(rd,n,1./ior);
  vec3 q=p-n*0.003; float thr=1.-F; float travel=0.;
  int nb = uQ==1 ? 5 : 3;
  for(int b=0;b<5;b++){ if(b>=nb) break;
    float t=0.;
    for(int i=0;i<48;i++){ float h=-gemD(q+d*t); if(h<0.0008) break; t+=max(h,0.003); if(t>2.) break; }
    q+=d*t; travel+=t;
    vec3 no=gemN(q);
    vec3 att=exp(-absorb*travel);
    vec3 dout=refract(d,-no,ior);
    if(dot(dout,dout)>0.){
      float Fo=fres(dot(dout,no), pow((ior-1.)/(ior+1.),2.));
      col+=thr*(1.-Fo)*att*env(dout);
      thr*=Fo;
    }
    d=reflect(d,-no); q+=d*0.003;
  }
  return col;
}
vec3 gemCol(vec3 p, vec3 rd){
  vec3 n=gemN(p);
  if(GK==1){
    vec3 absb=vec3(0.02);
    if(uQ==1){
      return 1.35*vec3(gemPass(p,n,rd,2.38,absb).r, gemPass(p,n,rd,2.42,absb).g, gemPass(p,n,rd,2.47,absb).b);
    }
    return 1.35*gemPass(p,n,rd,2.42,absb);
  }
  vec3 absb=-log(max(uGemCol,vec3(0.02)))*1.6;
  vec3 c=gemPass(p,n,rd,1.77,absb)*1.6*mix(vec3(1.),min(uGemCol*1.5,vec3(1.)),0.65);
  float ndv=max(dot(n,-rd),0.);
  return c+uGemCol*uGemCol*(0.04+0.16*pow(ndv,2.));
}

vec3 shadeObj(vec3 p, vec3 rd, float m, bool deep){
  if(m==2.) return gemCol(p,rd);
  vec3 n=calcN(p);
  float a=ao(p,n);
  if(m==1.) return metalCol(p,n,rd,deep)*(0.35+0.65*a);
  vec3 L=keyL();
  float dif=max(dot(n,L),0.);
  float sh = deep ? softShadow(p+n*0.003, L) : 1.;
  float ndv=max(dot(n,-rd),0.);
  vec3 sky=vec3(0.30)+0.5*vec3(max(studio(n).y,0.));
  if(m==3.){ // perla
    vec3 base=uGemCol;
    vec3 c=base*(0.10+sky*0.55+1.05*dif*sh);
    vec3 irid=0.5+0.5*cos(6.2831*(vec3(0.0,0.33,0.67)+ndv*1.6+0.2));
    c+=irid*0.08*(1.-ndv)+base*0.25*pow(1.-ndv,3.);
    c+=env(reflect(rd,n))*fres(ndv,0.05)*0.9;
    return c*a;
  }
  if(m==4.){ // jade
    float v=0.5+0.5*sin(p.x*9.+sin(p.y*7.+p.z*5.)*2.2);
    float v2=0.5+0.5*sin(p.y*23.+p.x*11.+sin(p.x*13.)*1.5);
    vec3 base=mix(uGemCol*0.7, uGemCol*1.8+0.02, v*0.45)*mix(0.85,1.1,v2);
    float wrap=max((dot(n,L)+0.45)/1.45,0.);
    vec3 c=base*(0.12+sky*0.45+0.95*wrap*mix(1.,sh,0.7));
    c+=uGemCol*0.6*pow(1.-ndv,2.)*0.5;
    c+=env(reflect(rd,n))*fres(ndv,0.05);
    return c*a;
  }
  if(m==5.){ // esfera
    float r=length(p.xy-vec2(0.,1.07));
    vec3 c=uGemCol*(0.25+0.6*dif) + env(reflect(rd,n))*fres(ndv,0.05)*0.06;
    c+= uGemCol*0.35*(0.5+0.5*cos(atan(p.y-1.07,p.x)*2.+1.))*smoothstep(0.5,0.0,r);
    return c*a;
  }
  if(m==6.){ // piel
    vec3 base=vec3(0.075,0.04,0.025);
    float g=0.85+0.15*hash(floor(p.xy*80.));
    return (base*g*(0.15+0.9*dif*sh)+env(reflect(rd,n))*0.03)*a;
  }
  if(m==8.){ // cordón
    return vec3(0.02)*(0.3+dif)+vec3(0.05)*pow(1.-ndv,2.);
  }
  return vec3(0.);
}

vec3 render(vec3 ro, vec3 rd){
  float m; vec3 col;
  float tf = rd.y<0. ? -ro.y/rd.y : 1e9;
  float t=trace(ro, rd, min(tf,40.), m);
  if(t>0.){
    vec3 p=ro+rd*t;
    if(m==7.){ // cristal del reloj
      vec3 n=calcN(p);
      vec3 refl=env(reflect(rd,n))*fres(max(dot(n,-rd),0.),0.04);
      noGlass=true;
      float m2; float t2=trace(p+rd*0.01, rd, 3., m2);
      vec3 under = t2>0. ? shadeObj(p+rd*(0.01+t2), rd, m2, uQ==1) : vec3(0.);
      noGlass=false;
      return under*0.96+refl;
    }
    return shadeObj(p, rd, m, uQ==1);
  }
  // piso de acrílico negro
  vec3 bg=vec3(0.012,0.012,0.016);
  if(tf<1e8){
    vec3 p=ro+rd*tf;
    vec2 off=p.xz-uTarget.xz;
    float pool=exp(-dot(off,off)*0.22);
    vec3 L=keyL();
    float sh = (uQ==1 && length(off)<BR+1.5) ? softShadow(p+vec3(0.,0.002,0.), L) : 1.;
    float occ=1.;
    if(uQ==1 && length(off)<BR+0.5){ occ=clamp(map(p).x*3.5+0.25,0.,1.); }
    col=vec3(0.035,0.034,0.04)*(0.25+1.8*pool)*mix(0.35,1.,sh)*occ;
    vec3 r=reflect(rd,vec3(0.,1.,0.));
    float F=fres(-rd.y,0.04)*0.9;
    float m2; float t2=trace(p+r*0.002, r, 6., m2);
    vec3 rc = t2>0. ? shadeObj(p+r*(0.002+t2), r, m2, false) : env(r)*0.15;
    col+=rc*F*exp(-max(t2,0.)*0.6)*(t2>0.?1.:0.4);
    col=mix(col, bg, 1.-exp(-tf*0.025));
    return col;
  }
  return bg+env(rd)*0.02;
}

vec3 aces(vec3 x){ return clamp((x*(2.51*x+0.03))/(x*(2.43*x+0.59)+0.14),0.,1.); }

void main(){
  T=uType; GK=uGem; YAW=uCam.x;
  BC=uTarget; BR = (T==2||T==6) ? 4.2 : (T==5 ? 2.0 : (T==7 ? 1.9 : 2.3));
  vec2 uv=(gl_FragCoord.xy-0.5*uRes)/uRes.y;
  vec3 ta=uTarget;
  vec3 ro=ta+uCam.z*vec3(sin(uCam.x)*cos(uCam.y), sin(uCam.y), cos(uCam.x)*cos(uCam.y));
  vec3 ww=normalize(ta-ro), uu=normalize(cross(ww,vec3(0.,1.,0.))), vv=cross(uu,ww);
  vec3 rd=normalize(uv.x*uu+uv.y*vv+3.2*ww);
  vec3 col=render(ro,rd);
  // viñeta y tono
  col*=1.0-0.35*dot(uv,uv);
  col=aces(col*1.15);
  col=pow(col,vec3(1./2.2));
  col+= (hash(gl_FragCoord.xy)-.5)/255.;
  fragColor=vec4(col,1.);
}
