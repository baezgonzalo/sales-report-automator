const archivo = document.getElementById('archivo');

archivo?.addEventListener('change', () => {
  if (archivo.files?.length) {
    archivo.form.requestSubmit();
  }
});
