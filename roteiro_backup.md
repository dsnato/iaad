## Parte 1: IntroduÃ§Ã£o e Contexto (Pessoa 1) â€” 2 minutos

**ExibiÃ§Ã£o na tela:** Slide de capa â†’ Estrutura do projeto no VS Code â†’ Streamlit rodando (Home).

### Roteiro
- â€œOlÃ¡, sou **[Nome P1]**. Nossa equipe desenvolveu um sistema de gestÃ£o para ClÃ­nicas MÃ©dicas, que organiza MÃ©dicos, Pacientes, ClÃ­nicas e Consultas.â€
- â€œAs ferramentas utilizadas foram:  
  **MySQL 8.0** para o banco de dados,  
  **Python** com `mysql-connector` para comunicaÃ§Ã£o com o banco,  
  **Streamlit** para interface grÃ¡fica.â€
- Mostrar rapidamente:
  - `requirements.txt`
  - inÃ­cio do cÃ³digo Python (importaÃ§Ãµes + conexÃ£o), sem se aprofundar.
- â€œA ideia foi manter o sistema simples e funcional, atendendo aos requisitos da atividade.â€

---

## Parte 2: Modelagem e DER (Pessoa 2) â€” 2 minutos

**ExibiÃ§Ã£o na tela:** MySQL Workbench â†’ Aba do Diagrama EER.

### Roteiro
- â€œSou **[Nome P2]**. Vou apresentar a modelagem do banco.â€
- â€œEste Ã© o **DER** gerado por engenharia reversa no MySQL Workbench.â€
- â€œA tabela **Consulta** funciona como entidade associativa principal, conectando MÃ©dico, Paciente e ClÃ­nica.â€
- â€œCardinalidades:  
  - Um mÃ©dico â†’ vÃ¡rias consultas  
  - Um paciente â†’ vÃ¡rias consultas  
  - Uma consulta â†’ pertence a uma Ãºnica clÃ­nicaâ€
- â€œA modelagem foi estruturada com chaves estrangeiras para garantir consistÃªncia e integridade dos dados.â€


