// registro_asistencia/frontend/static/js/talleres.js

document.addEventListener("DOMContentLoaded", function() {
  const script = document.getElementById("selIds");
  if (!script) return;
  let sel = [];
  try {
    sel = JSON.parse(script.textContent);
  } catch (e) {
    return;
  }
  sel.forEach(function(id) {
    const cb = document.querySelector('input[name="alumnos"][value="' + id + '"]');
    if (cb) cb.checked = true;
  });
});

