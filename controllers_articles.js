var SQLconnection = require("../config/database");
const bcryptjs = require("bcryptjs");
require("dotenv").config();
const jwt = require("jsonwebtoken");
const myfunctions = require("../Myfunctions/functions");
const { mailOptions, transport } = require("../config/email");
const { copynewtemplatedata } = require("./reference");
const { resend } = require("./eco");

module.exports = {
  show: function (req, res, next) {
    console.error("works");
    SQLconnection.query("select prodfdp.all_users.id,  prodfdp.company.city , prodfdp.company.state , prodfdp.company.country, prodfdp.all_roles.role_name,\
        prodfdp.purchase_orders.ports_in_india , prodfdp.invoices.invoice_doc , prodfdp.products.description_goods ,\
        case prodfdp.invoices.invoice_doc \
        when 'commercial_invoice' then prodfdp.commercial_invoice.final_destination \
        when 'custom_invoice' then prodfdp.custom_invoice.final_destination \
        when 'packing_list' then prodfdp.packing_list.final_destination \
        else null \
        end 'destination' \
        from prodfdp.all_users \
        inner join prodfdp.company on prodfdp.all_users.company_id = prodfdp.company.id \
        inner join prodfdp.purchase_orders on prodfdp.all_users.id = prodfdp.purchase_orders.exporter_id \
        inner join prodfdp.all_roles on prodfdp.all_users.role_id = prodfdp.all_roles.role_id    \
        inner join prodfdp.invoices on prodfdp.purchase_orders.invoice_number =  prodfdp.invoices.invoice_number  \
        inner join prodfdp.products on prodfdp.invoices.invoice_number = prodfdp.products.invoice_number  \
        left join prodfdp.custom_invoice on prodfdp.custom_invoice.invoice_number = prodfdp.invoices.invoice_number \
        and prodfdp.invoices.invoice_doc = 'custom_invoice' \
        left join prodfdp.commercial_invoice on prodfdp.commercial_invoice.invoice_number = prodfdp.invoices.invoice_number \
        and prodfdp.invoices.invoice_doc = 'commercial_invoice' \
        left join prodfdp.packing_list on prodfdp.packing_list.invoice_number = prodfdp.invoices.invoice_number \
        and prodfdp.invoices.invoice_doc = 'packing_list' \
        where prodfdp.all_users.id=?", [req.body.userId],
      function (err, userInfo) {
        if (err) {
            res.json({
                error : "error"
            })
          next(err);
        } else {
          if (JSON.stringify(userInfo) == JSON.stringify([])) {
            res
              .status(401)
              .json({ message: "User id Doesn't Exist", data: null });
          }
          else
          {
              console.log(userInfo)
              res.json({
                userInfo
            })
          }
        }
      }
    );
  },
};
