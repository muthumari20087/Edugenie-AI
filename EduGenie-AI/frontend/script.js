function openTab(id){
  document.querySelectorAll('.tab-content').forEach(t=>t.style.display='none');
  document.getElementById(id).style.display='block';
}

async function callAPI(type){
  const tabMap = {
    'ask': 'ask-tab',
    'explain': 'explain-tab',
    'quiz': 'quiz-tab',
    'path': 'path-tab',
    'summary': 'summary-tab'
  };

  // active tab ah kandupidi
  let activeTab = document.getElementById(tabMap[type]) || document.querySelector('.tab-content[style*="block"]');
  if(!activeTab) activeTab = document.body;

  let inputEl = activeTab.querySelector('input[type="text"], input:not([type]), textarea');
  let levelEl = activeTab.querySelector('select');
  let outputEl = activeTab.querySelector('div[id^="ans"], pre,.answer, p:last-of-type') || document.getElementById('ans'+type) || activeTab.lastElementChild;

  let value = inputEl? inputEl.value : "";
  if(!value){ alert("Topic/Question type pannu da macha!"); return; }

  let URL="", body={};
  if(type==='ask'){ URL='/api/ask'; body={question: value}; }
  if(type==='explain'){ URL='/api/explain'; body={topic: value, level: levelEl? levelEl.value : "beginner"}; }
  if(type==='quiz'){ URL='/api/quiz'; body={topic: value}; }
  if(type==='path'){ URL='/api/learning-path'; body={goal: value}; }
  if(type==='summary'){ URL='/api/summarize'; body={text: value}; }

  outputEl.innerHTML = "⏳ Generating da macha...";

  try{
    let res = await fetch(URL, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
    let data = await res.json();
    let finalText = data.explanation || data.answer || data.path || data.summary || (data.quiz? JSON.stringify(data.quiz, null, 2) : JSON.stringify(data, null, 2));
    outputEl.innerText = finalText;
  }catch(e){
    outputEl.innerText = "Error da: " + e.message;
    console.error(e);
  }
}