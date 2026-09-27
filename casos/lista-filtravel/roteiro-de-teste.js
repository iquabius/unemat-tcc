// Roteiro de teste da Lista filtrável, igual para as seis implementações web.
// Cole no console do navegador com o exemplo aberto; a última linha devolve
// o resultado de cada verificação ("ok" ou "FALHOU"). Segue a especificação
// do README.org.
(async () => {
  const esperar = () => new Promise((r) => setTimeout(r, 80));
  const controle = (n) => document.querySelector(`[name="${n}"], [formcontrolname="${n}"]`);
  const setter = (el) => Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  async function mudar(n, valor, evento) {
    const el = controle(n);
    setter(el).call(el, valor);
    el.dispatchEvent(new Event(evento, { bubbles: true }));
    await esperar();
  }
  const buscar = (texto) => mudar("busca", texto, "input");
  const escolher = (n, valor) => mudar(n, valor, "change");
  const texto = (el) => el.textContent.replace(/\s+/g, " ").trim();
  const nomes = () => [...document.querySelectorAll(".produtos .nome")].map(texto);
  const contagem = () => texto(document.querySelector(".contagem"));
  const vazio = () => {
    const p = document.querySelector(".vazio");
    return Boolean(p && !p.hidden);
  };
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(`${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`);

  await esperar();
  conferir("1 contagem inicial", contagem(), "30 de 30 produtos");
  conferir("1 ordem por nome", nomes().slice(0, 3), ["Açúcar mascavo 1 kg", "Agenda 2027", "Azeite extravirgem 500 ml"]);
  conferir("1 categorias", [...controle("categoria").options].map(texto), ["Todas", "Casa", "Cozinha", "Eletrônicos", "Mercearia", "Papelaria"]);
  conferir("1 sem aviso de vazio", vazio(), false);
  conferir("1 preço formatado", texto(document.querySelector(".produtos li .preco")), "R$ 12,50");

  await buscar("CAFE");
  conferir("2 busca sem acento e em maiúsculas", [contagem(), nomes()], ["2 de 30 produtos", ["Café em grãos 500 g", "Cafeteira italiana"]]);
  await buscar("  cerâmica ");
  conferir("3 busca com acento e espaços", nomes(), ["Caneca de cerâmica", "Vaso de cerâmica"]);

  await buscar("");
  await escolher("categoria", "Cozinha");
  await escolher("ordem", "maior-preco");
  conferir("4 cozinha por maior preço", nomes(), ["Chaleira elétrica", "Cafeteira italiana", "Frigideira antiaderente", "Faca do chef", "Tábua de corte", "Caneca de cerâmica"]);

  await escolher("categoria", "");
  await escolher("ordem", "menor-preco");
  conferir("5 todas por menor preço", [contagem(), nomes().slice(0, 2)], ["30 de 30 produtos", ["Chá de camomila", "Bloco de notas adesivas"]]);

  await buscar("xyz");
  conferir("6 nenhum resultado", [contagem(), nomes().length, vazio()], ["0 de 30 produtos", 0, true]);
  await buscar("");
  conferir("7 volta ao catálogo inteiro", [contagem(), vazio()], ["30 de 30 produtos", false]);

  return r.join("\n");
})()
