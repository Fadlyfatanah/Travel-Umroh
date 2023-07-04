from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CheckoutSkipPayment(WebsiteSale):
    @http.route()
    def payment_get_status(self, sale_order_id, **post):
        # When skip payment step, the transaction not exists so only render
        # the waiting message in ajax json call
        if request.website.website_sale_payment:
            return super().payment_get_status(sale_order_id, **post)
        return {
            "recall": True,
            "message": request.website._render(
                "ff_website_sale_without_payment.order_state_message"
            ),
        }

    @http.route()
    def payment_confirmation(self, **post):
        if request.website.website_sale_payment:
            return super().payment_confirmation(**post)
        order = (
            request.env["sale.order"]
            .sudo()
            .browse(request.session.get("sale_last_order_id"))
        )
        order.action_confirm()
        try:
            order._send_order_confirmation_mail()
        except Exception:
            return request.render(
                "ff_website_sale_without_payment.confirmation_order_error"
            )
        request.website.sale_reset()
        only_services = order.only_services
        return request.render("website_sale.confirmation", {"order": order, "only_services": only_services})
