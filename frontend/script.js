document.addEventListener('DOMContentLoaded', listarQuestoes);

function listarQuestoes() {
  fetch('http://localhost:8000/questoes')
    .then(response => response.json())
    .then(data => {
      const lista = document.getElementById('lista-questoes');
      lista.innerHTML = '';
      data.forEach(questao => {
        const item = document.createElement('li');
        item.id = `questao-${questao.id}`;
        item.innerHTML = `
          <strong>${questao.texto}</strong>
          <button onclick="deletarQuestao(${questao.id})">Deletar</button>
        `;
        lista.appendChild(item);
      });
    });
}

function deletarQuestao(id) {
  fetch(`http://localhost:8000/questoes/${id}`, {
    method: 'DELETE'
  })
  .then(response => {
    if (response.ok) {
      document.getElementById(`questao-${id}`).remove();
    } else {
      alert('Erro ao deletar a questão.');
    }
  })
  .catch(error => {
    console.error('Erro:', error);
  });
}
