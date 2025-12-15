document.addEventListener('DOMContentLoaded', () => { 

    //References
    const projectTableBody = document.querySelector('#projectTable tbody');

    const detailId = document.getElementById('detail-project-id');
    const detailName = document.getElementById('detail-project-name');
    const detailDesc = document.getElementById('detail-project-desc');
    const detailManager = document.getElementById('detail-project-manager-id');
    const detailBudget = document.getElementById('detail-project-budget');
    const detailStart = document.getElementById('detail-project-start');
    const detailEnd = document.getElementById('detail-project-end');
    const detailTeam = document.getElementById('detail-project-team');

    const btnSave = document.getElementById('btn-update-project');
    const btnNew = document.getElementById('btn-new-project');
    const btnDelete = document.getElementById('btn-delete-project');

    const milestoneModal = document.getElementById('milestoneModal');
    const milestoneTableBody = document.getElementById('milestoneTableBody');
    const milestoneModalCloseBtn = document.getElementById('milestoneModalCloseBtn');
    const milestoneProjectTitle = document.getElementById('milestoneProjectTitle');

    const workLogTbody = document.getElementById('worklog-tbody');
    const totalHoursSpan = document.getElementById('total-hours');

    const worklogEmployee = document.getElementById('new-worklog-employee');
    const worklogHours = document.getElementById('new-worklog-hours');
    const btnAddWorklog = document.getElementById('btn-add-worklog');

  
    let selectedProjectId = null;
    let selectedProjectRow = null;
    let selectedTeamIds = [];
    let selectedMilestones = [];
    let selectedWorkLogs = [];
    let allowMilestoneEditing = false;
    let allowWorkLogEditing = false;

    function parseTeamIds() {
        selectedTeamIds = detailTeam.value
            .split(',')
            .map(v => v.trim())
            .filter(v => v.length);
    }

    function applyStartDateLock() {
        const today = new Date();
        today.setHours(0,0,0,0);

        if (detailEnd.value) {
            const end = new Date(detailEnd.value);
            end.setHours(0,0,0,0);
         
            detailStart.disabled = end < today;
        } else {
           
            detailStart.disabled = false;
        }
    }

    function syncWorklogsToRow() {
        if (!selectedProjectRow) return;
        selectedProjectRow.dataset.projectWorklogs = JSON.stringify(selectedWorkLogs);
        updateProjectRowHours();
    }

    function syncMilestonesToRow() {
        if (!selectedProjectRow) return;
        selectedProjectRow.dataset.projectMilestones =
            JSON.stringify(selectedMilestones.filter(m => !m.editing));
    }
    //Update Project Hours
    function updateProjectRowHours() {
        if (!selectedProjectRow) return;
        const total = selectedWorkLogs.reduce((s, w) => s + parseFloat(w.hours || 0), 0);
        const cell = selectedProjectRow.querySelector('.project-total-hours');
        if (cell) cell.textContent = total.toFixed(2);
    }

    function clearProjectForm() {
        selectedProjectId = null;
        selectedProjectRow = null;
        selectedTeamIds = [];
        selectedMilestones = [];
        selectedWorkLogs = [];

        detailId.value = '';
        detailName.value = '';
        detailDesc.value = '';
        detailManager.value = '';
        detailBudget.value = '';
        detailStart.value = '';
        detailEnd.value = '';
        detailTeam.value = '';

        detailId.readOnly = false;      
        detailTeam.readOnly = false;    
        applyStartDateLock();           

        renderWorkLogs();
    }

    
    projectTableBody.addEventListener('click', e => {
        const row = e.target.closest('tr');
        if (!row?.dataset.projectId) return;

        selectedProjectRow = row;
        selectedProjectId = row.dataset.projectId;

        detailId.value = selectedProjectId;
        detailId.readOnly = true;      

        detailName.value = row.dataset.projectName || '';
        detailDesc.value = row.dataset.projectDesc || '';
        detailManager.value = row.dataset.projectManagerId || '';
        detailBudget.value = row.dataset.projectBudget || '';
        detailStart.value = row.dataset.projectStart || '';
        detailEnd.value = row.dataset.projectEnd || '';
        detailTeam.value = row.dataset.projectTeamIds || '';
        detailTeam.readOnly = false;    
        parseTeamIds();

        selectedMilestones = JSON.parse(row.dataset.projectMilestones || '[]');
        selectedWorkLogs = JSON.parse(row.dataset.projectWorklogs || '[]');
        //Start date lock for Projects with end date in past
        const end = detailEnd.value ? new Date(detailEnd.value) : null;
        const today = new Date(); today.setHours(0,0,0,0);
        allowMilestoneEditing = !end || end >= today;
        allowWorkLogEditing = allowMilestoneEditing;

        applyStartDateLock();
        renderWorkLogs();
    });
     
    detailEnd.addEventListener('change', applyStartDateLock);

  
    btnNew.addEventListener('click', e => {
        e.preventDefault();
        clearProjectForm();
    });
    //Save Project
    btnSave.addEventListener('click', e => {
        e.preventDefault();
        if (!detailId.value || !detailName.value) {
            return alert('Project ID and Name are required');
        }

        parseTeamIds();

        const payload = {
            new_project_id: detailId.value,
            name: detailName.value,
            description: detailDesc.value,
            manager_id: detailManager.value || null,
            budget: detailBudget.value || null,
            start_date: detailStart.value || null,
            end_date: detailEnd.value || null,
            team: selectedTeamIds
        };
        //Create or Update Project
        const url = selectedProjectId
            ? `/projects/${selectedProjectId}/update`
            : '/projects/create';

        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.ok ? location.reload() : alert('Save failed'));
    });
    //Delete Project
    btnDelete.addEventListener('click', e => {
        e.preventDefault();
        if (!selectedProjectId) return alert('Select a project first');
        if (!confirm('Delete this project?')) return;

        fetch(`/projects/${selectedProjectId}/delete`, { method: 'POST' })
            .then(() => location.reload());
    });

    //Worklogs
    function renderWorkLogs() {
        workLogTbody.innerHTML = '';

        if (!selectedWorkLogs.length) {
            workLogTbody.innerHTML =
                `<tr><td colspan="4" class="text-muted text-center">No worklogs</td></tr>`;
        } else {
            selectedWorkLogs.forEach((w, i) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${w.date}</td>
                    <td>${w.employee}</td>
                    <td>${w.hours}</td>
                    <td>
                        <button class="btn btn-sm btn-danger btn-delete-worklog"
                                data-id="${w.id}" data-index="${i}">
                            Delete
                        </button>
                    </td>`;
                workLogTbody.appendChild(tr);
            });
        }

        totalHoursSpan.textContent =
            selectedWorkLogs.reduce((s, w) => s + parseFloat(w.hours || 0), 0).toFixed(2);

        syncWorklogsToRow();
    }

    btnAddWorklog.addEventListener('click', () => {
        if (!allowWorkLogEditing) return alert('Project ended');

       
        if (!selectedProjectId) selectedProjectId = 'temp-new-project';

        const employee = worklogEmployee.value.trim();
        const hours = worklogHours.value.trim();
        if (!employee || !hours) return alert('Employee and hours required');

        fetch('/worklogs/create', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                project_id: selectedProjectId,
                employee,
                hours
            })
        })
        .then(res => res.json())
        .then(w => {
            if (!w.date) {
                const today = new Date();
                w.date = today.toISOString().split('T')[0];
            }

            selectedWorkLogs.push(w);
            renderWorkLogs();
            worklogEmployee.value = '';
            worklogHours.value = '';
        });
    });
    // Delete Worklog
    workLogTbody.addEventListener('click', e => {
        if (!e.target.classList.contains('btn-delete-worklog')) return;

        const id = e.target.dataset.id;
        const index = e.target.dataset.index;

        fetch(`/worklogs/${id}/delete`, { method: 'POST' })
            .then(() => {
                selectedWorkLogs.splice(index, 1);
                renderWorkLogs();
            });
    });

    //MILESTONES 

    function renderMilestones() {
        milestoneTableBody.innerHTML = '';
        milestoneProjectTitle.textContent = detailName.value || '';

        selectedMilestones.forEach((m, i) => {
            const tr = document.createElement('tr');
            tr.dataset.index = i;

            if (m.editing) {
                tr.innerHTML = `
                    <td><input class="form-control title" value="${m.title}"></td>
                    <td><input class="form-control desc" value="${m.description}"></td>
                    <td>
                        <select class="form-select status">
                            <option ${m.status==='Pending'?'selected':''}>Pending</option>
                            <option ${m.status==='In Progress'?'selected':''}>In Progress</option>
                            <option ${m.status==='Complete'?'selected':''}>Complete</option>
                        </select>
                    </td>
                    <td><input type="date" class="form-control date" value="${m.due_date||''}"></td>
                    <td>
                        <button class="btn btn-success save">Save</button>
                        <button class="btn btn-secondary cancel">Cancel</button>
                        <button class="btn btn-danger delete">Delete</button>
                    </td>`;
            } else {
                tr.innerHTML = `
                    <td>${m.title}</td>
                    <td>${m.description}</td>
                    <td>${m.status}</td>
                    <td>${m.due_date||''}</td>
                    <td>
                        <button class="btn btn-primary edit">Edit</button>
                        <button class="btn btn-danger delete">Delete</button>
                    </td>`;
            }
            milestoneTableBody.appendChild(tr);
        });

        milestoneTableBody.insertAdjacentHTML('beforeend', `
            <tr><td colspan="5" class="text-center">
                <button id="btn-add-milestone" class="btn btn-success">+ Add Milestone</button>
            </td></tr>
        `);
    }
    //View Milestones
    document.getElementById('btn-view-milestones').addEventListener('click', () => {
        if (!selectedProjectId) return alert('Select a project');
        renderMilestones();
        milestoneModal.style.display = 'block';
    });

    milestoneModalCloseBtn.addEventListener('click', () => {
        syncMilestonesToRow();
        milestoneModal.style.display = 'none';
    });
    //Milestone Table Actions
    milestoneTableBody.addEventListener('click', e => {
        const tr = e.target.closest('tr');
        const i = tr?.dataset.index;
        const m = selectedMilestones[i];

        if (e.target.classList.contains('edit')) { m.editing = true; renderMilestones(); }
        if (e.target.classList.contains('cancel')) { m.editing = false; renderMilestones(); }

        if (e.target.classList.contains('save')) {
            m.title = tr.querySelector('.title').value;
            m.description = tr.querySelector('.desc').value;
            m.status = tr.querySelector('.status').value;
            m.due_date = tr.querySelector('.date').value;

            const url = m.id ? `/milestones/${m.id}/update` : '/milestones/create';
            fetch(url, {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({...m, project_id: selectedProjectId})
            })
            .then(res => res.json())
            .then(data => {
                Object.assign(m, data);
                m.editing = false;
                renderMilestones();
                syncMilestonesToRow();
            });
        }

        if (e.target.classList.contains('delete')) {
            if (!m.id) {
                selectedMilestones.splice(i,1);
                renderMilestones();
                return;
            }
            fetch(`/milestones/${m.id}/delete`, { method:'POST' })
                .then(() => {
                    selectedMilestones.splice(i,1);
                    renderMilestones();
                    syncMilestonesToRow();
                });
        }

        if (e.target.id === 'btn-add-milestone') {
            selectedMilestones.push({
                title:'', description:'', status:'Pending', due_date:'', editing:true
            });
            renderMilestones();
        }
    });

});
