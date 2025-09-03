(function($) {
    $(function() {
        const sizeSelect = $("#id_sizes");          // MultiSelect (MultiSelectField)
        const hiddenJson = $("#id_size_stock_json"); // Hidden input that carries the rows
        if (!sizeSelect.length || !hiddenJson.length) return;

        // Hide the hidden json field in the form row (it's already hidden input, but ensure)
        hiddenJson.closest(".form-row, .form-group").hide();

        // Build UI container right after the size field
        const ui = $(`
            <div class="size-stock-ui" style="margin-top:8px;">
                <button type="button" class="button add-sizes-btn">Add</button>
                <div class="size-stock-table-wrap" style="margin-top:10px;">
                    <table class="size-stock-table" style="width:100%;border-collapse:collapse;">
                        <thead>
                            <tr>
                                <th style="border:1px solid #ddd;padding:6px;text-align:left;">Size</th>
                                <th style="border:1px solid #ddd;padding:6px;text-align:left;">Stock</th>
                                <th style="border:1px solid #ddd;padding:6px;text-align:left;">Action</th>
                            </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
                <div class="size-stock-hint" style="margin-top:6px;color:#666;">
                    Select sizes above, then click <b>Add</b> to create rows. Duplicates are ignored.
                </div>
            </div>
        `);

        // Insert UI after the sizes field
        sizeSelect.closest(".form-row, .form-group, .field-sizes").append(ui);

        const tbody = ui.find("tbody");
        const addBtn = ui.find(".add-sizes-btn");

        // Parse/Save helpers
        function getData() {
            try { return hiddenJson.val() ? JSON.parse(hiddenJson.val()) : []; }
            catch(e) { return []; }
        }
        function setData(rows) {
            hiddenJson.val(JSON.stringify(rows));
        }

        // Render table from data
        function render() {
            const rows = getData();
            tbody.empty();
            rows.forEach((row, idx) => {
                const tr = $(`
                    <tr data-size="${row.size}">
                        <td style="border:1px solid #ddd;padding:6px;">${String(row.size).toUpperCase()}</td>
                        <td style="border:1px solid #ddd;padding:6px;">
                            <input type="number" class="stock-input" min="0" style="width:100px;"
                                   value="${parseInt(row.stock || 0, 10)}" />
                        </td>
                        <td style="border:1px solid #ddd;padding:6px;">
                            <button type="button" class="button delete-row-btn">Remove</button>
                        </td>
                    </tr>
                `);
                tbody.append(tr);
            });
        }

        // Initial state: if editing, backend pre-filled hidden JSON; render it
        render();

        // ADD button -> add rows for currently selected sizes (no duplicates)
        addBtn.on("click", function() {
            const selected = Array.from(sizeSelect[0].selectedOptions || []).map(o => o.value);
            if (!selected.length) return;

            const rows = getData();
            const existing = new Set(rows.map(r => r.size));
            let changed = false;

            selected.forEach(size => {
                if (!existing.has(size)) {
                    rows.push({ size: size, stock: 0 });
                    existing.add(size);
                    changed = true;
                }
            });

            if (changed) {
                setData(rows);
                render();
            } else {
                // Optional: brief inline note; avoiding alert() for smoother UX
                // You can add a small message here if you want
            }
        });

        // Update JSON when stock changes
        tbody.on("input", ".stock-input", function() {
            const tr = $(this).closest("tr");
            const size = tr.data("size");
            const value = parseInt($(this).val(), 10) || 0;

            const rows = getData();
            const row = rows.find(r => r.size === size);
            if (row) {
                row.stock = value;
                setData(rows);
            }
        });

        // Remove row
        tbody.on("click", ".delete-row-btn", function() {
            const tr = $(this).closest("tr");
            const size = tr.data("size");
            let rows = getData();
            rows = rows.filter(r => r.size !== size);
            setData(rows);
            render();
        });
    });
})(django.jQuery);
