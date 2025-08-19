Ferramenta web para MySQL construída com Python, Streamlit e Docker.

## Funcionalidades

### Settings
- **Configure Parameters:**
  - Customização de parâmetros com interface web simples e intuitiva (Streamlit).

### Account
- **Create or Reset Account:**
  - Criação de usuários e reset de senha com mensagens e parâmetros customizáveis.

### Backups Tables
- **Table Local Backup:**
  - Exporta tabelas/views do MySQL em CSV, com ou sem compactação, localmente em `app/outputdir` usando o utilitário `util.exportTable()` do MySQL Shell.
- **Table S3 Backup:**
  - Exporta tabelas/views do MySQL em CSV, com ou sem compactação, diretamente para o S3 conforme o bucket escolhido, usando o utilitário `util.exportTable()` do MySQL Shell.

### Benchmark
- **Performance Tests:**
  - Testes de performance de queries com o utilitário `mysqlslap`.

### Schemaspy
- **Documentação do Banco:**
  - (Futuro) Integração com SchemaSpy para geração de documentação do banco.