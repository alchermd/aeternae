$(document).ready(function () {
    fetch("/dashboard/employees/")
        .then(res => res.json())
        .then(json => {
            const columns = json.columns.map(column => ({title: column}));
            const data = json.data;

            $('#dataTable').DataTable({
                columns: columns,
                data: data,
            });
        })
});
