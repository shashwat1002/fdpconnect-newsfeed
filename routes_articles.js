const express = require("express");
const router = express.Router();
var cors = require("cors");

const articlesController = require('../controllers/articles');

router.post('/show', cors(), articlesController.show);
router.post('/data', cors(), articlesController.data);


module.exports = router;
