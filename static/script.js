function confirmDelete() {
    return confirm("آیا مطمئن هستید که می‌خواهید فایل‌های انتخاب شده را حذف کنید؟");
}

function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  if (fileInput.files.length === 0) {
      alert('لطفاً یک فایل انتخاب کنید.'); // پیام خطا اگر هیچ فایلی انتخاب نشده باشد
      return;
  }
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  // ارسال داده‌ها به سرور با استفاده از Fetch API
  fetch('/upload', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (response.ok) {
          alert('فایل با موفقیت آپلود شد.');
          // بعد از آپلود موفق، به صفحه داشبورد بروید
          window.location.href = '/dashboard'; // URL صفحه داشبورد را به اینجا اضافه کنید
      } else {
          alert('خطا در آپلود فایل.');
      }
  })
  .catch(error => {
      console.error('خطا:', error);
  });
}

function showFileName() {
  const fileInput = document.getElementById('fileInput');
  const fileNameDisplay = document.getElementById('fileName');

  // بررسی اینکه آیا فایلی انتخاب شده است
  if (fileInput.files.length > 0) {
      const fileName = fileInput.files[0].name; // گرفتن نام فایل
      fileNameDisplay.textContent = `فایل انتخاب شده: ${fileName}`; // نمایش نام فایل
  } else {
      fileNameDisplay.textContent = ''; // پاک کردن نام فایل در صورت عدم انتخاب
  }
}


document.querySelectorAll(".navList").forEach(function(element) {
    element.addEventListener('click', function() {
      
      document.querySelectorAll(".navList").forEach(function(e) {
        e.classList.remove('active');
    });

      // Add active class to the clicked navList element
      this.classList.add('active');
  
      // Get the index of the clicked navList element
      var index = Array.from(this.parentNode.children).indexOf(this);
  
      // Hide all data-table elements
      document.querySelectorAll(".data-table").forEach(function(table) {
        table.style.display = 'none';
      });
  
      // Show the corresponding table based on the clicked index
      var tables = document.querySelectorAll(".data-table");
      if (tables.length > index) {
        tables[index].style.display = 'block';
      }
    });
  });
  