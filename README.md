# 📊 MCP Server - Personal Expense Manager

An MCP (Model Context Protocol) server for managing and analyzing personal expenses from CSV files.

## 🚀 Features

- **Add expenses** to a CSV file with categorization
- **Get recent expenses** with day-based filtering
- **MCP Resource** for direct access to all expenses
- **Specialized prompt** that generates automatic analytical summaries
- **Analysis by category and payment method**
- **Trend detection and spending patterns**

## 📋 Requirements

```bash
pip install fastmcp mcp
```

## 🗂️ Project Structure

```
expenses-mcp-server/
├── server.py              # Main MCP server
├── data/
│   └── expenses.csv      # Expenses file (created automatically)
├── requirements.txt
└── README.md
```

## 🛠️ Installation & Usage

### 1. Clone or create the project

```bash
mkdir expenses-mcp-server
cd expenses-mcp-server
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install fastmcp mcp
```

### 4. Run the server

```bash
python server.py
```

## 🔧 Available Functionalities

### Tools

#### 1. `agregar_gasto` (Add Expense)
Adds a new expense to the system.

**Parameters:**
- `fecha`: Date in 'YYYY-MM-DD' format
- `categoria`: Expense category (e.g., "Food", "Transport")
- `cantidad`: Expense amount (float)
- `metodo_pago`: Payment method used

**Example:**
```python
agregar_gasto("2024-01-15", "Groceries", 150.75, "Debit Card")
```

#### 2. `obtener_gastos_recientes` (Get Recent Expenses)
Gets expenses from the last N days.

**Parameters:**
- `dias`: Number of days to query (default: 5)

**Example:**
```python
obtener_gastos_recientes(7)  # Last 7 days
```

### Resource

#### `resource://gastos`
Direct access to all stored expenses.

### Specialized Prompt

#### `Resumen de Gastos Recientes` (Recent Expenses Summary)
Generates a prompt with structured data for AI to create a complete analysis including:

- 📈 Statistical calculations (totals, averages)
- 🏷️ Category analysis
- 💳 Payment method distribution
- 🔍 Trend identification
- 💡 Personalized recommendations

## 📊 CSV Structure

The `data/expenses.csv` file has the following structure:

```csv
fecha,categoria,cantidad,metodo_pago
2024-01-15,Groceries,150.75,Debit Card
2024-01-16,Transport,45.50,Cash
2024-01-17,Entertainment,89.99,Credit Card
```

## 🔌 MCP Client Integration

### Python Client Example

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # Add expense
            result = await session.call_tool(
                "agregar_gasto",
                {
                    "fecha": "2024-01-18",
                    "categoria": "Restaurant", 
                    "cantidad": 85.50,
                    "metodo_pago": "Credit Card"
                }
            )
            print(result)
            
            # Get recent expenses
            expenses = await session.call_tool(
                "obtener_gastos_recientes", 
                {"dias": 5}
            )
            print(expenses)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎯 Use Cases

### 1. **Daily Expense Tracking**
```bash
# Add transport expense
agregar_gasto("2024-01-18", "Transport", 35.00, "Cash")

# Add food expense
agregar_gasto("2024-01-18", "Food", 120.00, "Debit Card")
```

### 2. **Weekly Analysis**
```bash
# Get last week summary
obtener_gastos_recientes(7)
```

### 3. **Monthly Report**
```bash
# Complete 30-day analysis
obtener_gastos_recientes(30)
```

## 📈 Example Generated Analysis

The specialized prompt generates analysis like:

```
📊 EXPENSE SUMMARY - LAST 5 DAYS

💰 TOTAL SPENT: $1,245.75
📅 DAILY AVERAGE: $249.15
🔢 TRANSACTIONS: 8 purchases

🏷️ CATEGORY DISTRIBUTION:
• Groceries: 45% ($560.25)
• Transport: 25% ($311.44)  
• Entertainment: 20% ($249.15)
• Restaurant: 10% ($124.58)

💳 PAYMENT METHODS:
• Credit Card: 60%
• Debit Card: 30%
• Cash: 10%

📈 OBSERVATIONS:
• Highest spending on Wednesday ($420.50)
• "Groceries" category represents almost half of expenses
• Growing trend in credit card usage

💡 RECOMMENDATIONS:
• Consider bulk purchases to reduce grocery expenses
• Diversify payment methods for better control
• Set weekly limit for entertainment
```

## 🛠️ Troubleshooting

### Error: "FileNotFoundError"
- Ensure the `data/` directory exists
- Server creates the file automatically with the first expense

### Error: "Encoding issues"
- Server uses UTF-8 for special character compatibility

### Error: "Invalid date format"
- Use exact format: `YYYY-MM-DD`
- Example: `2024-01-18`

## 📝 License

MIT License

## 📞 Support

For issues and questions, open a ticket in the project repository.

---

**Start tracking your expenses intelligently!** 🚀