import frappe
from frappe import _

def get_context(context):
    user = frappe.session.user

    if user == "Guest":
        frappe.redirect("/login")
        return

    context.title = "📚 Meus Projectos"
    print("Usuário atual:", user)

    context.projects = frappe.get_all(
        "BookProject",
        filters={"autor": user},  # ou "owner": user, se for o caso
        fields=["titulo", "data_de_criacao", "descricao", "autor", "creation", "status"],
        order_by="creation desc"
    )
