<template>
  <div class="operadoras-container">
    <h1>Consulta de Operadoras de Saúde</h1>
    
    <div class="search-container">
      <input
        type="text"
        v-model="searchTerm"
        placeholder="Digite razão social ou nome fantasia"
        @keyup.enter="fetchOperadoras"
        class="search-input"
      />
      <select v-model="selectedUf" class="uf-select">
        <option value="">Todos os estados</option>
        <option v-for="uf in ufList" :value="uf" :key="uf">{{ uf }}</option>
      </select>
      <button @click="fetchOperadoras" class="search-button">Buscar</button>
    </div>

    <div v-if="loading" class="loading">Carregando...</div>
    
    <div v-else>
      <div class="results-info">
        {{ operadoras.length }} operadoras encontradas
      </div>
      
      <table class="operadoras-table">
        <thead>
          <tr>
            <th>Registro</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>Cidade</th>
            <th>UF</th>
            <th>Telefone</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="op in operadoras" :key="op.registro_operadora">
            <td>{{ op.registro_operadora }}</td>
            <td>{{ op.razao_social }}</td>
            <td>{{ op.nome_fantasia || '-' }}</td>
            <td>{{ op.cidade || '-' }}</td>
            <td>{{ op.uf }}</td>
            <td>{{ op.telefone || '-' }}</td>
            <td>
              <button @click="showDetails(op.registro_operadora)" class="details-button">
                Detalhes
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showModal = false">&times;</span>
        <h2>Detalhes da Operadora</h2>
        <div v-if="operadoraDetalhes" class="details-grid">
          <div><strong>Registro ANS:</strong> {{ operadoraDetalhes.registro_operadora }}</div>
          <div><strong>CNPJ:</strong> {{ operadoraDetalhes.cnpj }}</div>
          <div><strong>Razão Social:</strong> {{ operadoraDetalhes.razao_social }}</div>
          <div><strong>Nome Fantasia:</strong> {{ operadoraDetalhes.nome_fantasia || '-' }}</div>
          <div><strong>Modalidade:</strong> {{ operadoraDetalhes.modalidade || '-' }}</div>
          <div><strong>Representante:</strong> {{ operadoraDetalhes.representante || '-' }}</div>
          <div><strong>Telefone:</strong> {{ operadoraDetalhes.telefone || '-' }}</div>
          <div><strong>Email:</strong> {{ operadoraDetalhes.email || '-' }}</div>
          <div><strong>Data Registro:</strong> {{ operadoraDetalhes.data_registro }}</div>
          <div><strong>Cidade/UF:</strong> {{ operadoraDetalhes.cidade || '-' }}/{{ operadoraDetalhes.uf }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'OperadorasPage',
  data() {
    return {
      searchTerm: '',
      selectedUf: '',
      operadoras: [],
      loading: false,
      showModal: false,
      operadoraDetalhes: null,
      ufList: [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
      ]
    }
  },
  methods: {
    async fetchOperadoras() {
      this.loading = true;
      try {
        const params = {};
        if (this.searchTerm) {
          params.razao_social = this.searchTerm;
          params.nome_fantasia = this.searchTerm;
        }
        if (this.selectedUf) {
          params.uf = this.selectedUf;
        }
        
        const response = await axios.get('http://localhost:8000/operadoras/', { params });
        this.operadoras = response.data.results;
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error);
        alert('Erro ao buscar operadoras. Verifique o console para detalhes.');
      } finally {
        this.loading = false;
      }
    },
    async showDetails(registro) {
      try {
        const response = await axios.get(`http://localhost:8000/operadoras/${registro}`);
        this.operadoraDetalhes = response.data;
        this.showModal = true;
      } catch (error) {
        console.error('Erro ao buscar detalhes:', error);
        alert('Erro ao buscar detalhes da operadora.');
      }
    }
  },
  mounted() {
    this.fetchOperadoras();
  }
}
</script>

<style scoped>
.operadoras-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
}

.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.uf-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.search-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.search-button:hover {
  background-color: #369f6b;
}

.results-info {
  margin: 15px 0;
  font-size: 14px;
  color: #666;
}

.operadoras-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.operadoras-table th {
  background-color: #42b983;
  color: white;
  padding: 12px;
  text-align: left;
}

.operadoras-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
}

.operadoras-table tr:hover {
  background-color: #f5f5f5;
}

.details-button {
  padding: 5px 10px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.details-button:hover {
  background-color: #1a2a3a;
}

.loading {
  text-align: center;
  padding: 20px;
  font-style: italic;
  color: #666;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 5px;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 20px;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-top: 20px;
}

.details-grid div {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}
</style>