import frappe
from frappe import _

def get_context(context):
    project_name = frappe.form_dict.project_name
    user = frappe.session.user

    if user == "Guest":
        frappe.redirect("/login")
        return
    print("nome: ", project_name)

    if not frappe.db.exists("BookProject", {"titulo": project_name, "autor": user}):
        frappe.throw(_("Projeto não encontrado ou você não tem permissão."), frappe.PermissionError)

    project = frappe.get_doc("BookProject", project_name)

    chapters = frappe.get_all(
        "BookChapter",
        filters={"refbookprojectrefbookproject": project.titulo},
        fields=["ordem", "titulo", "conteudo"],
    )

    context.project = project
    context.chapters = chapters
    context.title = f"📖 {project.titulo}"