// Admin Dashboard

document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    
    // Export button
    document.getElementById('export-btn').addEventListener('click', exportData);
});

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`/api/admin/stats?t=${Date.now()}`, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        const data = await response.json();
        
        // Update total responses
        document.getElementById('total-responses').textContent = data.total_responses;
        
        // Find most common type
        const mostCommon = Object.entries(data.personality_counts)
            .sort((a, b) => b[1] - a[1])[0];
        
        if (mostCommon) {
            const typeName = data.personality_types[mostCommon[0]].name;
            document.getElementById('most-common-type').textContent = typeName;
        }
        
        // Render personality chart
        renderPersonalityChart(data.personality_counts, data.personality_types);
        
        // Render responses table
        renderResponsesTable(data.recent_customers);
        
    } catch (error) {
        console.error('Error loading stats:', error);
        alert('Erro ao carregar estatísticas');
    }
}

// Render personality distribution chart
function renderPersonalityChart(counts, types) {
    const chartContainer = document.getElementById('personality-chart');
    chartContainer.innerHTML = '';
    
    const total = Object.values(counts).reduce((sum, count) => sum + count, 0);
    
    Object.entries(types).forEach(([key, typeInfo]) => {
        const count = counts[key] || 0;
        const percentage = total > 0 ? (count / total) * 100 : 0;
        
        const barContainer = document.createElement('div');
        barContainer.className = 'chart-bar';
        
        const label = document.createElement('div');
        label.className = 'chart-label';
        label.textContent = typeInfo.name;
        
        const barFill = document.createElement('div');
        barFill.className = 'chart-bar-fill';
        barFill.style.backgroundColor = typeInfo.color;
        barFill.style.width = `${percentage}%`;
        barFill.textContent = `${percentage.toFixed(1)}%`;
        
        const countText = document.createElement('div');
        countText.className = 'chart-count';
        countText.textContent = count;
        
        barContainer.appendChild(label);
        barContainer.appendChild(barFill);
        barContainer.appendChild(countText);
        
        chartContainer.appendChild(barContainer);
    });
}

// Render responses table
function renderResponsesTable(customers) {
    const tbody = document.getElementById('responses-body');
    tbody.innerHTML = '';
    
    if (customers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="loading-cell">Nenhuma resposta ainda</td></tr>';
        return;
    }
    
    customers.forEach(customer => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${customer.name}</td>
            <td>${customer.email || '-'}</td>
            <td>${customer.whatsapp || '-'}</td>
            <td>${customer.birthday || '-'}</td>
            <td>${customer.personality_type}</td>
            <td>${customer.created_at}</td>
        `;
        
        tbody.appendChild(row);
    });
}

// Export data
async function exportData() {
    try {
        const response = await fetch(`/api/admin/export/excel?t=${Date.now()}`, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        if (!response.ok) {
            throw new Error('Falha ao gerar arquivo Excel');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `natforms-export-${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error('Error exporting data:', error);
        alert('Erro ao exportar dados');
    }
}

// Auto-refresh every 30 seconds
setInterval(loadStats, 30000);
