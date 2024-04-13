var url_for_classes = "";
if (`{{current_user.role}}` == "Student") {
    url_for_classes = "/get-student-classes";
    $("#class_join").on("click", function (e) {
        window.location.href = "/join-class";
    });
} else {
    url_for_classes = "/get-teacher-classes";
    $("#class_create").on("click", function (e) {
        window.location.href = "/create-class";
    });
}

// Side Class

$.ajax({
    url: url_for_classes,
    type: "POST",
    success: function (resp) {
        if (resp != "Problem") {
            for (item in resp) {
                var class_html = "";
                var class_name = resp[item]["class_name"].trim();
                if (`{{current_user.role}}` == "Student") {
                    if (resp[item]["class_name"].trim().length > 20) {
                        class_name = class_name.substr(0, 18) + "....";
                    } else {
                        class_name = class_name;
                    }
                } else {
                    if (
                        (resp[item]["class_name"].trim() + resp[item]["class_standard"])
                            .length > 20
                    ) {
                        class_name =
                            class_name.substr(0, 15) + "...." + resp[item]["class_standard"];
                    } else {
                        class_name = class_name + resp[item]["class_standard"];
                    }
                }

                class_html = `<div class="submenu collapsed" id="${resp[item]["classid"]}""> <a class="nav-link" href="/class/${resp[item]["classid"]}/">
                    <div class="nav-link-icon "> <i-feather class="icon" style="width: 1rem !important;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="feather feather-book-open">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path> <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path> </svg></i-feather> </div>
                    ${class_name} </a> </div >`;
                $("#classes_content").append(class_html);
            }
        } 
        else {
            var class_html = `<div class="alert alert-danger alert-dismissible fade show" role="alert"> There is some problem in contacting to the server! Try again after some time.
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span</button> </div>`;
            $(".flashes").append(class_html);
        }
    },
    error: function () {
        alert("Problem in getting classes");
    },
});
