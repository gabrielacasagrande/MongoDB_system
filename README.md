**Passo 1: Estratégia de Particionamento de Dados** 

**1.1 Particionamento Horizontal (Sharding)*** 

**Justificativa:** 

O particionamento horizontal distribui os dados de uma coleção em diferentes shards, com cada shard contendo um subconjunto dos documentos. 

Essa abordagem é escalável porque permite adicionar novos shards facilmente à medida que o volume de dados cresce. 

É eficiente para consultas e atualizações localizadas, pois os dados podem ser distribuídos com base em um campo comum, como a filial ou a localização geográfica. 

**Implementação:** 

**Shard Key:** Escolha a filial (**store\_id**) como a chave de shard. Isso garante que todos os produtos de uma filial específica sejam mantidos juntos em um shard. 

**Balancer:** Configure o balancer do MongoDB para redistribuir os shards conforme necessário para manter um balanceamento de carga uniforme. 

{

"\_id": ObjectId, 

"store\_id": "string", // Shard key 

"product\_id": "string", 

"product\_name": "string", 

"category": "string", 

"quantity": Number, 

"price": Number, 

"last\_updated": ISODate 

} 



**1.2 Particionamento Vertical*** 

**Justificativa:** 

O particionamento vertical divide os dados em diferentes coleções ou bancos de dados com base em campos específicos. 

Esta abordagem é útil para separar dados que são frequentemente acessados juntos de dados que não são. 

**Implementação:** 

**Core Data Collection:** Contém informações básicas e frequentemente acessadas dos produtos. 

**Extended Data Collection:** Contém dados adicionais e menos acessados, como histórico de vendas ou detalhes do fornecedor. 

// **Core Data Collection** 

{ 

"\_id": ObjectId, 

"store\_id": "string", 

"product\_id": "string", 

"product\_name": "string", 

"category": "string", 

"quantity": Number, 

"price": Number 

} 



// **Extended Data Collection** 

{ 

"\_id": ObjectId, 

"product\_id": "string", // Foreign key reference 

"supplier": "string", 

"sales\_history": [ 

{ "date": ISODate, "quantity\_sold": Number } 

] 

} 

**Passo 2: Implementação Simulada** 

**2.1 Gerar Dados Simulados*** 

Foi utilizado Python com a biblioteca **Faker** para gerar um grande volume de dados simulados. 

**2.2 Importações e Configurações Iniciais:** 

Importamos as bibliotecas  

**Faker**: Biblioteca para gerar dados falsos (nomes, endereços, datas, etc.). 

**random**: Biblioteca para gerar números aleatórios. 

**pymongo**: Biblioteca para interagir com o MongoDB. 

**2.3 Configurações de Conexão ao MongoDB**: 

Se já tiver um ambiente instalado no mongoDB: 

Define o nome de usuário, senha e o nome do banco de dados. 

Cria uma string de conexão para se conectar ao MongoDB com autenticação. 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.001.png) 

**2.4 Conectar ao MongoDB**: 

**pymongo.MongoClient(connection\_string)**: Cria um cliente MongoDB usando a string de conexão. 

**db = client[database\_name]**: Seleciona o banco de dados **supermarket**. 

**core\_collection** e **extended\_collection**: Seleciona as coleções **core\_data** e **extended\_data**, respectivamente. 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.002.png)

**2.5 Geração de Dados Simulados:** 

Criamos listas **core\_data\_list** e **extended\_data\_list** para armazenar os dados gerados. 

Usamos um loop para gerar 1.000.000 de registros simulados. 

Para cada iteração, geramos **store\_id** e **product\_id** únicos usando **fake.uuid4()**. 

Criamos um dicionário **core\_data** com os detalhes principais do produto. 

Criamos um dicionário **extended\_data** com detalhes adicionais do produto, incluindo o histórico de vendas. 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.003.png)

**2.6 Resultado:** 

O banco **surpermarket** foi criado com as respectivas coleções 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.004.png)   

Coleção **core\_data** com **610076** dados. 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.005.png)



Coleção **extended\_data** com **610075** dados. 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.006.png)

**Passo 3: Testes de Desempenho** 

**3.1 Consultas de Estoque*** 

Teste a eficiência das consultas de estoque utilizando diferentes filtros e índices. 

**Exemplo usado:** 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.007.png)

// **Exemplo de consulta de estoque** 

db.core\_data.find({ store\_id: "d5e12b31-cbd0-482c-bfa7-8dcd5b6d6dec", product\_id: "c167617f-fe98-4b06-99fc-f1e8aaf07a3e" }) 

**Resultado:** 

![](Aspose.Words.1a3c6c5b-2362-4f7f-a89c-f165e930a514.008.png)

**3.2 Atualizações de Inventário*** 

Teste as atualizações de inventário para verificar a eficiência das operações de escrita. 

// **Exemplo de atualização de inventário** 

db.core\_data.updateOne( 

{ store\_id: "d5e12b31-cbd0-482c-bfa7-8dcd5b6d6dec", product\_id: "c167617f-fe98-4b06-99fc-f1e8aaf07a3e" }, 

{ $set: { quantity: 50, last\_updated: new Date() } }) 

**Resultado:** 

**3.3 Adição de Novas Filiais** 

Simule a adição de novas filiais e a redistribuição de dados. 

//**Simulação de adição de nova filial**  

db.core\_data.insertMany([ 

{  

"store\_id": "A10",  

"product\_id": "A10",  

"product\_name": "carne vermelha",  

"category": "carnes",  

"quantity": 100,  

"price": 19.99  

}, ]) 

**Resultado**: 

Consultei o estoque

**Conclusão** 

Este plano fornece uma estrutura para projetar um sistema de gerenciamento de estoque escalável e eficiente para uma cadeia de supermercados utilizando MongoDB. A estratégia de particionamento, implementação simulada e testes de desempenho garantirão que o sistema atenda aos requisitos de escalabilidade e eficiência. 
