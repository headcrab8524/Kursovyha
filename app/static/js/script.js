$(document).ready(function () {
  $(".form-validatable").on("submit", function (e) {
    e.preventDefault();

    const url = $(this).attr("action");
    const type = $(this).attr("method");

    $.ajax({
      url: url,
      type: type,
      data: new FormData(this),
      processData: false,
      contentType: false,
      success: () => {
        window.location = $(this).data("next");
      },
      error: (response) => {
        const errors = response.responseJSON;

        $(this).find(".input-errors").text("");

        let isFocused = false;
        for (let key in errors) {
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

  if ($(".mod-page-description").length) {
    $(".mod-page-description").html($(".mod-page-description").eq(0).text());
    $(".mod-page-description").removeClass("d-none");
  }
});
