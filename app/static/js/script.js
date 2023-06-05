$(document).ready(function () {
  $(".form-validatable").on("submit", function (e) {
    e.preventDefault();

    const url = $(this).attr("action");
    const type = $(this).attr("method");

    console.log("url:" + url);
    console.log("type:" + type);

    $.ajax({
      url: url,
      type: type,
      data: new FormData(this),
      processData: false,
      contentType: false,
      success: () => {
        window.location.reload();
      },
      error: (response) => {
        const errors = response.responseJSON;

        $(this).find(".input-errors").text("");

        let isFocused = false;
        for (let key in errors) {
          // фокус на первый инпут с ошибкой (если есть)
          if (!isFocused) {
            isFocused = true;
            const input = $(this).find("#" + key);
            if (input) {
              input.focus();
            }
          }

          // вывод ошибок
          const errorMessages = errors[key];
          console.log(errorMessages);

          $(this)
            .find(`.input-errors[data-input="${key}"]`)
            .text(errorMessages.join("\n"));
        }
      },
    });
  });

  $(".form-validatable input").on("input", function (e) {
    console.log("gg");
    const inputName = $(this).attr("name");
    $(this)
      .closest("form")
      .find(`.input-errors[data-input="${inputName}"]`)
      .text("");
  });
});
