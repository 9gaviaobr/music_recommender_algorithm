const $ = (sel) => document.querySelector(sel);
const tracksEl = $("#tracks");
const resultsEl = $("#results");
const formEl = $("#prefs-form");

async function fetchJSON(url){
  const res = await fetch(url, {headers: {"Accept":"application/json"}});
  if(!res.ok) throw new Error("Request failed: "+res.status);
  return await res.json();
}

function trackRow(t){
  const div = document.createElement('div');
  div.className = 'track';
  const meta = document.createElement('div');
  meta.className = 'meta';
  const title = document.createElement('div');
  title.className = 'title';
  title.textContent = `${t.title}`;
  const sub = document.createElement('div');
  sub.className = 'sub';
  sub.textContent = `${t.artist} · ${t.genre} · ${t.year}`;
  meta.appendChild(title);
  meta.appendChild(sub);
  const actions = document.createElement('div');
  actions.className = 'actions';
  const btn = document.createElement('button');
  btn.className = 'btn';
  btn.textContent = 'Recommend similar';
  btn.addEventListener('click', async () => {
    await recommendFromSeed(t.id);
  });
  actions.appendChild(btn);
  div.appendChild(meta);
  div.appendChild(actions);
  return div;
}

function renderResults(recs){
  resultsEl.innerHTML = '';
  if(!recs || recs.length === 0){
    resultsEl.textContent = 'No recommendations found.';
    return;
  }
  for(const t of recs){
    resultsEl.appendChild(trackRow(t));
  }
}

async function loadTracks(){
  try{
    const data = await fetchJSON('/api/tracks');
    tracksEl.innerHTML = '';
    for(const t of data.tracks){
      tracksEl.appendChild(trackRow(t));
    }
  }catch(e){
    tracksEl.textContent = 'Failed to load tracks.';
  }
}

async function recommendFromSeed(seed){
  try{
    const data = await fetchJSON(`/api/recommend?seed=${encodeURIComponent(seed)}&k=5`);
    renderResults(data.recommendations);
  }catch(e){
    resultsEl.textContent = 'Failed to fetch recommendations.';
  }
}

formEl.addEventListener('submit', async (e) => {
  e.preventDefault();
  const d = $('#danceability').value;
  const en = $('#energy').value;
  const v = $('#valence').value;
  const t = $('#tempo').value;
  try{
    const url = `/api/recommend?danceability=${d}&energy=${en}&valence=${v}&tempo=${t}&k=5`;
    const data = await fetchJSON(url);
    renderResults(data.recommendations);
  }catch(err){
    resultsEl.textContent = 'Failed to fetch recommendations.';
  }
});

loadTracks();


