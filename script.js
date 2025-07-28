document.addEventListener('DOMContentLoaded', () => {
    fetch('transactions.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('transactions-container');
            data.forEach(transaction => {
                const transactionDiv = document.createElement('div');
                transactionDiv.classList.add('transaction');

                const item = document.createElement('p');
                item.textContent = `Item: ${transaction.item}`;

                const quantity = document.createElement('p');
                quantity.textContent = `Quantity: ${transaction.quantity}`;

                const paid = document.createElement('p');
                paid.textContent = `Paid: Rs ${transaction.paid}`;

                const change = document.createElement('p');
                change.textContent = `Change: Rs ${transaction.change}`;

                const date = document.createElement('p');
                date.textContent = `Date: ${new Date(transaction.date).toLocaleString()}`;

                transactionDiv.appendChild(item);
                transactionDiv.appendChild(quantity);
                transactionDiv.appendChild(paid);
                transactionDiv.appendChild(change);
                transactionDiv.appendChild(date);

                container.appendChild(transactionDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
            const container = document.getElementById('transactions-container');
            container.textContent = 'Could not load transactions. Make sure the transactions.json file exists and is accessible.';
        });
});