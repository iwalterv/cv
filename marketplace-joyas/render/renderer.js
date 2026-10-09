// Minimal WebGL2 jewel renderer shared by bake + page
function makeJewelRenderer(canvas, fragSrc){
  const gl = canvas.getContext('webgl2',{preserveDrawingBuffer:true,antialias:false});
  if(!gl) return null;
  const vs = `#version 300 es
in vec2 p; void main(){ gl_Position=vec4(p,0.,1.); }`;
  function sh(t,s){ const o=gl.createShader(t); gl.shaderSource(o,s); gl.compileShader(o); if(!gl.getShaderParameter(o,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER,vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER,fragSrc)); gl.linkProgram(pr);
  if(!gl.getProgramParameter(pr,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
  gl.useProgram(pr);
  const b=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,b); gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(pr,'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const U={}; ['uRes','uType','uGem','uMetal','uGemCol','uCam','uTarget','uQ','uSeed'].forEach(n=>U[n]=gl.getUniformLocation(pr,n));
  function set(s){
    gl.uniform2f(U.uRes, canvas.width, canvas.height);
    gl.uniform1i(U.uType, s.type); gl.uniform1i(U.uGem, s.gem);
    gl.uniform3fv(U.uMetal, s.metal); gl.uniform3fv(U.uGemCol, s.gemCol);
    gl.uniform3fv(U.uCam, s.cam); gl.uniform3fv(U.uTarget, s.target);
    gl.uniform1i(U.uQ, s.q|0); gl.uniform1f(U.uSeed, s.seed||0);
  }
  return {
    gl,
    draw(s){ gl.viewport(0,0,canvas.width,canvas.height); set(s); gl.disable(gl.SCISSOR_TEST); gl.drawArrays(gl.TRIANGLES,0,3); },
    async drawTiled(s, tile=128){
      gl.viewport(0,0,canvas.width,canvas.height); set(s); gl.enable(gl.SCISSOR_TEST);
      for(let y=0;y<canvas.height;y+=tile) for(let x=0;x<canvas.width;x+=tile){
        gl.scissor(x,y,tile,tile); gl.drawArrays(gl.TRIANGLES,0,3);
        const px=new Uint8Array(4); gl.readPixels(x,y,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);
        await new Promise(r=>setTimeout(r,0));
      }
      gl.disable(gl.SCISSOR_TEST);
    }
  };
}
