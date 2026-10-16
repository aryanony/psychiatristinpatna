(()=>{
const WA='917070474808',D=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],S=[[540,720],[900,1140]];
const $=id=>document.getElementById(id);
const t=m=>{const h=Math.floor(m/60);return (h%12||12)+':'+String(m%60).padStart(2,'0')+' '+(h<12?'am':'pm')};
function ist(){const p={};new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Kolkata',weekday:'long',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date()).forEach(x=>p[x.type]=x.value);return{day:D.indexOf(p.weekday),min:(+p.hour%24)*60+ +p.minute}}
function status(){const n=ist(),el=$('state');
 if(n.day>0)for(const[a,b]of S)if(n.min>=a&&n.min<b){el.className='state open';$('state-t').textContent='Open now, until '+t(b);return}
 for(let o=0;o<8;o++){const d=(n.day+o)%7;if(d===0)continue;for(const[a]of S)if(o>0||a>n.min){el.className='state';$('state-t').textContent='Closed now. Opens '+(o===0?'today':o===1?'tomorrow':D[d])+' at '+t(a);return}}}
if($('state')){status();setInterval(status,60000)}

// Mobile Hamburger Menu & Drawer Controller
const menuBtn = $('menu-btn'), drawer = $('mobile-nav'), closeBtn = $('mobile-close-btn'), backdrop = $('mobile-backdrop');
if (menuBtn && drawer) {
  function openDrawer() {
    drawer.hidden = false;
    drawer.offsetHeight;
    drawer.classList.add('is-open');
    menuBtn.setAttribute('aria-expanded', 'true');
    document.body.classList.add('drawer-locked');
    if (closeBtn) closeBtn.focus();
  }
  function closeDrawer() {
    drawer.classList.remove('is-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('drawer-locked');
    setTimeout(() => {
      if (!drawer.classList.contains('is-open')) drawer.hidden = true;
    }, 300);
  }
  menuBtn.addEventListener('click', () => {
    menuBtn.getAttribute('aria-expanded') === 'true' ? closeDrawer() : openDrawer();
  });
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', closeDrawer));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menuBtn.getAttribute('aria-expanded') === 'true') {
      closeDrawer();
      menuBtn.focus();
    }
  });
  const mql = window.matchMedia('(min-width: 52.01rem)');
  mql.addEventListener('change', e => {
    if (e.matches && menuBtn.getAttribute('aria-expanded') === 'true') closeDrawer();
  });
}

const f=$('req'),dt=$('d');if(!f)return;
dt.min=new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Kolkata'});
function bad(first,id,eid,msg){$(id).setAttribute('aria-invalid','true');$(eid).textContent=msg;return first||id}
function clear(){['n','p','d'].forEach(i=>$(i).removeAttribute('aria-invalid'));['en','ep','ed'].forEach(i=>$(i).textContent='')}
f.addEventListener('submit',e=>{e.preventDefault();clear();
 const name=$('n').value.replace(/\s+/g,' ').trim(),ph=$('p').value.replace(/[\s\-()]/g,''),date=dt.value,sess=$('s').value;let first=null;
 if(name.length<2)first=bad(first,'n','en','Enter your name so the clinic knows who to ask for.');
 if(!(/^(?:\+?91|0)?[6-9]\d{9}$/.test(ph)||/^\+\d{8,15}$/.test(ph)))first=bad(first,'p','ep','Enter a phone number the clinic can call, for example 7070474808.');
 if(date){const w=new Date(date+'T00:00:00').getDay();if(date<dt.min)first=bad(first,'d','ed','Choose today or a later date.');else if(w===0)first=bad(first,'d','ed','No Sunday hours are published. Choose Monday to Saturday.')}
 if(first){$(first).focus();return}
 const m=['Appointment request','Name: '+name,'Phone: '+ph,'Preferred date: '+(date||'Any'),'Preferred session: '+sess].join('\n');
 $('msg').textContent=m;$('wa').href='https://wa.me/'+WA+'?text='+encodeURIComponent(m);$('cpn').textContent='';
 const r=$('result');r.hidden=false;r.focus();r.scrollIntoView({block:'nearest'});
});
$('cp').addEventListener('click',()=>{const m=$('msg').textContent,n=$('cpn');
 (navigator.clipboard?navigator.clipboard.writeText(m):Promise.reject()).then(()=>n.textContent='Message copied.',()=>n.textContent='Copying was blocked. Select the message above and copy it by hand.')});
})();
