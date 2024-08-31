$("form[name=signup_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/home";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/home";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=reg_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/regform",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/user/dashboard/";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=collector_signup_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/collector/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/collector/login/";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=collector_login_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/collector/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/collector/dashboard/";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=admin_signup_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/admin/login";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=admin_login_form]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/admin/panel";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=blood_search_starter]").submit(function (e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/resolvedistance",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp)
      window.location.href = "/waiting";
    },
    error: function (resp) {
      console.log(resp)
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});