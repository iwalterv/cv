const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const dir=__dirname; const frag=fs.readFileSync(dir+'/jewel.frag','utf8'); const rjs=fs.readFileSync(dir+'/renderer.js','utf8');
const jobs=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); const out=process.argv[3]; const W=+process.argv[4]||800, H=+process.argv[5]||1000, SS=+process.argv[6]||2;
fs.mkdirSync(out,{recursive:true});
(async()=>{
  const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const p=await b.newPage(); p.on('console',m=>console.log('page:',m.text())); p.on('pageerror',e=>console.log('ERR',e.message));
  await p.setContent('<canvas id=c></canvas><canvas id=d></canvas>');
  await p.addScriptTag({content:rjs});
  for(const j of jobs){
    const t0=Date.now();
    const data=await p.evaluate(async ({j,frag,W,H,SS})=>{
      const c=document.getElementById('c'); c.width=W*SS; c.height=H*SS;
      if(!window.R){ window.R=makeJewelRenderer(c,frag); }
      await window.R.drawTiled({...j,q:1},160);
      const d=document.getElementById('d'); d.width=W; d.height=H; const x=d.getContext('2d'); x.imageSmoothingQuality='high'; x.drawImage(c,0,0,W,H);
      return d.toDataURL('image/jpeg',0.86);
    },{j,frag,W,H,SS});
    fs.writeFileSync(path.join(out,j.name+'.jpg'), Buffer.from(data.split(',')[1],'base64'));
    console.log(j.name, ((Date.now()-t0)/1000).toFixed(1)+'s');
  }
  await b.close();
})();
