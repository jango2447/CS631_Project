document.addEventListener('DOMContentLoaded', function () {

    const btnSetStatus = document.getElementById('btn-set-status');
    btnSetStatus.addEventListener('click', async () => {
        console.log('Set Status button clicked');
        const empNo = detailEmpNo.textContent.trim();
        if (!empNo) {
            alert("Please select an employee first.");
            return;
        }

        // Determine new status based on button text
        const setToInactive = btnSetStatus.textContent === 'Set to Inactive';
        const newStatus = !setToInactive; // If button says Set to Inactive, newStatus = false (inactive)

        try {
            const response = await fetch('/set-status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ employee_no: empNo, is_active: newStatus })
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.error || 'Failed to update status');

            // Update button text and color based on new status
            if (newStatus) {
                btnSetStatus.textContent = 'Set to Inactive';
                btnSetStatus.style.backgroundColor = '#f8d7da';
                btnSetStatus.style.color = '#842029';
                btnSetStatus.classList.remove('btn-secondary');
                btnSetStatus.classList.add('btn-danger');
            } else {
                btnSetStatus.textContent = 'Set to Active';
                btnSetStatus.style.backgroundColor = '#d1e7dd';
                btnSetStatus.style.color = '#0f5132';
                btnSetStatus.classList.remove('btn-secondary');
                btnSetStatus.classList.add('btn-success');
            }

            // Update employee row is_active cell text
            const selectedRow = document.querySelector(`#employeeTable tbody tr[data-employee-no="${empNo}"]`);
            if (selectedRow) {
                selectedRow.querySelector('td:nth-child(8)').textContent = newStatus ? 'Yes' : 'No';

                // Update Employment End Date column (7th column)
                const endDateCell = selectedRow.querySelector('td:nth-child(7)');
                if (endDateCell) {
                    endDateCell.textContent = data.employment_end_date || '';
                }
            }

            alert('Employee status updated successfully.');

        } catch (err) {
            alert('Error updating status: ' + err.message);
        }
    });


    // ADD EMPLOYEE MODAL LOGIC
    const addEmployeeBtn = document.getElementById('btn-add-employee');
    const addEmployeeModal = document.getElementById('addEmployeeModal');
    const addEmployeeCloseBtn = document.getElementById('add-employee-close-btn');
    const addEmployeeCancel = document.getElementById('add-employee-cancel');

    if (addEmployeeCancel) {
        addEmployeeCancel.addEventListener('click', () => {
            document.getElementById('addEmployeeModal').style.display = 'none';
        });
    }
    if (addEmployeeBtn && addEmployeeModal) {
        addEmployeeBtn.addEventListener('click', () => {
            addEmployeeModal.style.display = 'flex';
        });
    }

    if (addEmployeeCloseBtn) {
        addEmployeeCloseBtn.addEventListener('click', () => {
            addEmployeeModal.style.display = 'none';
        });
    }

    window.addEventListener('click', e => {
        if (e.target === addEmployeeModal) {
            addEmployeeModal.style.display = 'none';
        }
    });

    // SAVE EMPLOYEE
    const saveEmployeeBtn = document.getElementById('add-employee-save');

    if (saveEmployeeBtn) {
        saveEmployeeBtn.addEventListener('click', async () => {

            const name = document.getElementById('add-emp-name').value.trim();
            const title = document.getElementById('add-emp-title').value.trim();
            const departmentName = document.getElementById('add-emp-department').value; // renamed
            const salaryType = document.getElementById('add-salary-type').value;
            const salary = document.getElementById('add-salary-amount').value;

            if (!name || !title || !departmentName || !salaryType || !salary) {
                return alert("Please fill out all fields.");
            }

            const payload = {
                name,
                title,
                department_name: departmentName,  // send department_name as string
                salary_type: salaryType,
                salary: salary
            };

            try {
                const response = await fetch("/add-employee", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Failed to add employee");
                }

                // Close modal
                document.getElementById('addEmployeeModal').style.display = 'none';

                alert("Employee added successfully!");

                // Optional: refresh page or table later
                location.reload();

            } catch (err) {
                alert(err.message);
            }
        });
    }

    const rows = document.querySelectorAll('#employeeTable tbody tr');
    const detailEmpNo = document.getElementById('detail-empno');
    const detailName = document.getElementById('detail-name');
    const detailSalaryType = document.getElementById('detail-salary-type');
    const detailCurrentSalary = document.getElementById('detail-current-salary');
    const inputNewSalary = document.getElementById('input-new-salary');
    const inputPercentIncrease = document.getElementById('input-percent-increase');

    let currentSalary = 0;

    rows.forEach(row => {
        row.addEventListener('click', () => {

            const empNo = row.getAttribute('data-employee-no') || '';
            const empName = row.getAttribute('data-employee-name') || '';
            const salaryType = row.getAttribute('data-salary-type') || '';
            const currentSalaryStr = row.getAttribute('data-current-salary') || '';

            currentSalary = parseFloat(currentSalaryStr) || 0;
            detailEmpNo.textContent = empNo;
            detailName.textContent = empName;
            detailSalaryType.textContent = salaryType ? salaryType.charAt(0).toUpperCase() + salaryType.slice(1) : "N/A";
            detailCurrentSalary.textContent = currentSalary > 0 ? `$${currentSalary.toFixed(2)}` : 'N/A';

            inputNewSalary.value = '';
            inputPercentIncrease.value = '';

            const isActive = row.querySelector('td:nth-child(8)').textContent.trim() === 'Yes';
            const btnSetStatus = document.getElementById('btn-set-status');
            if (btnSetStatus) {
                if (isActive) {
                    btnSetStatus.textContent = 'Set to Inactive';
                    btnSetStatus.style.backgroundColor = '#f8d7da';  // light red background
                    btnSetStatus.style.color = '#842029';            // dark red text for contrast
                    btnSetStatus.classList.remove('btn-secondary');
                    btnSetStatus.classList.add('btn-danger');
                } else {
                    btnSetStatus.textContent = 'Set to Active';
                    btnSetStatus.style.backgroundColor = '#d1e7dd';  // light green background
                    btnSetStatus.style.color = '#0f5132';            // dark green text for contrast
                    btnSetStatus.classList.remove('btn-secondary');
                    btnSetStatus.classList.add('btn-success');
                }
            }
        });
    });

    inputNewSalary.addEventListener('input', () => {
        const newSalary = parseFloat(inputNewSalary.value);
        if (!isNaN(newSalary) && currentSalary > 0) {
            const percentIncrease = ((newSalary - currentSalary) / currentSalary) * 100;
            inputPercentIncrease.value = percentIncrease.toFixed(2);
        } else {
            inputPercentIncrease.value = '';
        }
    });

    inputPercentIncrease.addEventListener('input', () => {
        const percent = parseFloat(inputPercentIncrease.value);
        if (!isNaN(percent) && currentSalary > 0) {
            const newSalary = currentSalary * (1 + (percent / 100));
            inputNewSalary.value = newSalary.toFixed(2);
        } else {
            inputNewSalary.value = '';
        }
    });

    // SET NEW SALARY BUTTON
    document.getElementById("btn-set-salary").addEventListener("click", function () {

        const empNo = detailEmpNo.textContent.trim();
        const newSalary = inputNewSalary.value.trim();
        const percent = inputPercentIncrease.value.trim();

        if (!empNo) return alert("Please select an employee first.");

        if (!newSalary && !percent) return alert("Please enter a new salary or percent increase.");

        const payload = {
            employee_no: empNo,
            new_salary: newSalary,
            percent_increase: percent
        };

        fetch("/set-salary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
            .then(res => res.json())
            .then(data => {
                document.getElementById("salary-msg").innerHTML =
                    `<div class="alert alert-success">${data.message}</div>`;

                const selectedEmpNo = detailEmpNo.textContent.trim();
                const selectedRow = document.querySelector(`#employeeTable tbody tr[data-employee-no="${selectedEmpNo}"]`);

                if (selectedRow) {
                    selectedRow.setAttribute('data-current-salary', data.new_salary);
                    selectedRow.setAttribute('data-salary-type', data.salary_type);

                    detailCurrentSalary.textContent = `$${parseFloat(data.new_salary).toFixed(2)}`;
                    currentSalary = parseFloat(data.new_salary);
                    inputNewSalary.value = '';
                    inputPercentIncrease.value = '';
                }
            })
            .catch(err => {
                document.getElementById("salary-msg").innerHTML =
                    `<div class="alert alert-danger">Error updating salary.</div>`;
            });
    });

    // SALARY HISTORY MODAL LOGIC
    const modal = document.getElementById('salaryHistoryModal');
    const yearSelect = document.getElementById('yearSelect');
    const btnViewHistory = document.getElementById('btn-view-history');
    const btnGetData = document.getElementById('btn-get-data');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const historyTableContainer = document.getElementById('historyTableContainer');
    const historyTableBody = document.getElementById('historyTableBody');

    btnViewHistory.addEventListener('click', () => {
        const empNo = detailEmpNo.textContent.trim();

        if (!empNo) return alert("Please select an employee first.");

        historyTableBody.innerHTML = '';
        historyTableContainer.style.display = 'none';
        yearSelect.innerHTML = '';

        const row = document.querySelector(`#employeeTable tbody tr[data-employee-no="${empNo}"]`);
        if (!row) return;

        const startDateStr = row.querySelector('td:nth-child(6)').textContent.trim();
        const endDateStr = row.querySelector('td:nth-child(7)').textContent.trim();

        if (!startDateStr) return alert('Employment start date not found.');

        const startYear = new Date(startDateStr).getFullYear();
        const endYear = endDateStr ? new Date(endDateStr).getFullYear() : new Date().getFullYear();

        for (let y = startYear; y <= endYear; y++) {
            const option = document.createElement('option');
            option.value = y;
            option.textContent = y;
            yearSelect.appendChild(option);
        }

        modal.style.display = 'block';
    });

    modalCloseBtn.addEventListener('click', () => modal.style.display = 'none');

    window.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none'; });

    btnGetData.addEventListener('click', async () => {
        const selectedYear = yearSelect.value;
        if (!selectedYear) return alert('Please select a year.');

        const empNo = detailEmpNo.textContent.trim();

        if (!empNo) return alert('Please select an employee first.');

        try {

            const response = await fetch(`/salary-history/${empNo}/${selectedYear}`);
            if (!response.ok) throw new Error('Failed to fetch salary history');
            const data = await response.json();
            historyTableBody.innerHTML = '';
            const existingFooter = historyTableContainer.querySelector('tfoot');
            if (existingFooter) existingFooter.remove();

            let totalSalary = 0;
            let totalFedTax = 0;
            let totalStateTax = 0;
            let totalOtherTaxes = 0;
            let totalTakeHome = 0;

            data.monthly_salary_history.forEach(item => {
                const monthName = new Date(data.year, item.month - 1).toLocaleString('default', { month: 'long' });

                totalSalary += item.salary;
                totalFedTax += item.federal_tax;
                totalStateTax += item.state_tax;
                totalOtherTaxes += item.other_taxes;
                totalTakeHome += item.take_home;

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${monthName}</td>
                    <td>$${item.salary.toFixed(2)}</td>
                    <td>$${item.federal_tax.toFixed(2)}</td>
                    <td>$${item.state_tax.toFixed(2)}</td>
                    <td>$${item.other_taxes.toFixed(2)}</td>
                    <td>$${item.take_home.toFixed(2)}</td>
                `;
                historyTableBody.appendChild(tr);
            });

            // Create footer row for totals
            const tfoot = document.createElement('tfoot');
            tfoot.innerHTML = `
                <tr style="font-weight: bold; background-color: #f8f9fa;">
                    <td>Total</td>
                    <td>$${totalSalary.toFixed(2)}</td>
                    <td>$${totalFedTax.toFixed(2)}</td>
                    <td>$${totalStateTax.toFixed(2)}</td>
                    <td>$${totalOtherTaxes.toFixed(2)}</td>
                    <td>$${totalTakeHome.toFixed(2)}</td>
                </tr>
            `;

            historyTableContainer.querySelector('table').appendChild(tfoot);
            historyTableContainer.style.display = 'block';

        } catch (error) { alert('Error loading salary data: ' + error.message); }
    });
});
