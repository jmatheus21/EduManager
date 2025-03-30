const criarGeradorMenu = (configPadrao) => (entidade, configPersonalizado = {}) => {
  const config = { ...configPadrao, ...configPersonalizado };
  return config.itens.map(item => ({
    nome: item.nome,
    url: `/${entidade}${item.url}`
  }));
};

// Configuração padrão
export const criarMenuPadrao = criarGeradorMenu({
  itens: [
    { nome: "Consultar", url: "" },
    { nome: "Cadastrar", url: "/cadastrar" }
  ]
});

// Configuração customizada
export const criarMenuCustom = criarGeradorMenu({
  itens: [
    { nome: "Cadastrar", url: "" },
    { nome: "Alterar", url: "/alterar" }
  ]
});

// Menu simples
export const criarMenuSimples = criarGeradorMenu({
  itens: [
    { nome: "Consultar", url: "" }
  ]
});

export const criarMenuMatricular = criarGeradorMenu({
  itens: [
    { nome: "Consultar", url: "" }
  ]
});
