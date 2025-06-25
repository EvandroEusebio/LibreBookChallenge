$(document).ready(function () {
	const form = $("#addChapterForm");
	const formMessages = $("#form-messages");
	const project_name = "{{ book_project.titulo }}"; // Pega o nome do projeto do contexto Jinja

	form.on("submit", function (e) {
		e.preventDefault();

		formMessages.hide().removeClass("alert-success alert-danger").text("");

		const title = $("#title").val();
		const order = $("#order").val();
		const content = $("#content").val();

		if (!title || !order) {
			showMessage("danger", "Por favor, preencha o título e a order do capítulo.");
			return;
		}

		const submitButton = form.find(".btn-submit");
		submitButton.prop("disabled", true).text("Criando Capítulo...");

		frappe.call({
			method: "libre.api.create_chapter", // Nome completo do método
			args: {
				project_name: project_name,
				title: title,
				order: order,
				content: content,
			},
			callback: function (r) {
				submitButton.prop("disabled", false).text("Criar Capítulo");

				if (r.message) {
					showMessage("success", "Capítulo criado com sucesso!");
					window.location.href = `/chapter?project_name=${project_name}`;
				} else {
					const errorMessage = r.exc
						? JSON.parse(r.exc)._error_message || "Erro desconhecido"
						: "Erro desconhecido";
					showMessage("danger", `Erro: ${errorMessage}`);
				}
			},
			error: function (err) {
				submitButton.prop("disabled", false).text("Criar Capítulo");
				showMessage("danger", `Erro de rede ou servidor: ${err.statusText || err}`);
			},
		});
	});

	function showMessage(type, message) {
		formMessages
			.text(message)
			.addClass("alert-" + type)
			.fadeIn();
	}
});
