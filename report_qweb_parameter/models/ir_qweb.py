# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import ValidationError


class IrQWeb(models.AbstractModel):
    _inherit = "ir.qweb"

    def check_length(self, value, min_length=False, max_length=False):  # noqa
        """No use staticmethod because self is needed to translate exception messages"""
        if min_length and len(value) < min_length:
            raise ValidationError(
                self.env._("Length cannot be less than %s") % str(min_length)
            )
        if max_length and len(value) > max_length:
            raise ValidationError(
                self.env._("Length cannot be more than %s") % str(max_length)
            )
        return value

    def _compile_directive_esc(self, el, compile_context, level):
        min_value = el.attrib.pop("t-minlength", False)
        max_value = el.attrib.pop("t-maxlength", False)
        if min_value or max_value:
            el.attrib["t-esc"] = (
                'docs.env["ir.qweb"].check_length('
                + el.attrib["t-esc"]
                + ", "
                + (min_value or "False")
                + ", "
                + (max_value or "False")
                + ")"
            )
        if "t-length" in el.attrib:
            tlength = el.attrib.pop("t-length")
            el.attrib["t-esc"] = "(" + el.attrib["t-esc"] + ")[:" + tlength + "]"
        return super()._compile_directive_esc(el, compile_context, level)

    def _compile_directive_out(self, el, compile_context, level):
        min_value = el.attrib.pop("t-minlength", False)
        max_value = el.attrib.pop("t-maxlength", False)
        if min_value or max_value:
            el.attrib["t-out"] = (
                'docs.env["ir.qweb"].check_length('
                + el.attrib["t-out"]
                + ", "
                + (min_value or "False")
                + ", "
                + (max_value or "False")
                + ")"
            )
        if "t-length" in el.attrib:
            tlength = el.attrib.pop("t-length")
            el.attrib["t-out"] = "(" + el.attrib["t-out"] + ")[:" + tlength + "]"
        return super()._compile_directive_out(el, compile_context, level)

    def _compile_directive_raw(self, el, compile_context, level):
        # TODO: t-raw is deprecated, can it be removed?
        min_value = el.attrib.pop("t-minlength", False)
        max_value = el.attrib.pop("t-maxlength", False)
        if min_value or max_value:
            el.attrib["t-raw"] = (
                'docs.env["ir.qweb"].check_length('
                + el.attrib["t-raw"]
                + ", "
                + (min_value or "False")
                + ", "
                + (max_value or "False")
                + ")"
            )
        if "t-length" in el.attrib:
            tlength = el.attrib.pop("t-length")
            el.attrib["t-raw"] = "(" + el.attrib["t-raw"] + ")[:" + tlength + "]"
        return super()._compile_directive_raw(el, compile_context, level)
