/* Shared, seek-safe motion helpers. No clock: the registered GSAP timeline owns time. */
window.TravelMotion = {
  draw(tl, selector, at, duration) {
    const targets = typeof selector === 'string' ? document.querySelectorAll(selector) : [selector];
    targets.forEach(el => {
      const n=el.getTotalLength();
      tl.fromTo(el,{strokeDasharray:n,strokeDashoffset:n},{strokeDashoffset:0,duration,ease:'power2.inOut'},at);
    });
  },
  movePath(tl, selector, points, at, duration) {
    const lengths=points.slice(1).map((p,i)=>Math.hypot(p[0]-points[i][0],p[1]-points[i][1]));
    const sum=lengths.reduce((a,b)=>a+b,0)||1;
    let cue=at;
    points.slice(1).forEach((p,i)=>{
      const d=duration*lengths[i]/sum;
      tl.fromTo(selector,{x:points[i][0],y:points[i][1]},{x:p[0],y:p[1],duration:d,ease:'none',immediateRender:i===0},cue);
      cue+=d;
    });
  }
};
