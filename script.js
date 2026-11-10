const chat = document.getElementById("formChat")
const mensagens = document.getElementById("mensagens")
 
chat.addEventListener("submit", async function (e) {
    e.preventDefault();
    const texto = document.getElementById("mensagem").value.trim();
    if (texto === "") {return}
    mensagens.innerHTML += `<div class="msg-usuario">
    ${texto.replace(/&/g, "&amp;")
        .replace(/>/g, "&lt;")
        .replace(/</g, "&gt;")}
        </div>`
        texto.value = ""
 
        try {
            const resposta = await fetch("/api/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({mensagem: texto})
            })
            const dados = await resposta.json();
            if(!resposta.ok) {
                throw new Error(dados.erro)
            }
            mensagens.innerHTML += `
            <div class="mensagem-bot">
            ${dados.resposta}
            </div>
            `
        } catch (erro) {
            mensagens.innerHTML += `
            <div class="mensagem-bot">
            ${erro.message}
            </div>`
        }
        mensagens.scrollTop = mensagens.scrollHeight;
})
