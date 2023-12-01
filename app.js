const express = require('express');
const ejs = require('ejs')
const app = express();
var bodyParser = require('body-parser')
var session = require('express-session')

require('dotenv').config()

const mysql = require('mysql2')
const connection = mysql.createConnection({
    host : 'localhost',
    user : 'root',
    password : '1234',
    database : 'credit'
})
console.log('Connected to Mysql')

//connection.query("SET time_zone = 'Asia/Seoul'")

app.listen(8080, function(){
   console.log('listening on 8080') 
});

app.set('vies engine', 'ejs')
app.set('views', './views')


app.use(bodyParser.urlencoded({extended:false}))
app.use(express.static(__dirname+'/public'))
app.use(session({secret:'credit', cookie:{
    maxAge:60000}, resave:true, saveUninitialized:true
}))

app.use((req,res,next)=>{

    res.locals.user_id="";
    res.locals.name="";
    if(req.session.member){
        res.locals.user_id = req.session.member.user_id
        res.locals.name = req.session.member.name
    }
    next()
})

app.get('/', function(req, res){
    console.log(req.session.member);
    res.render('index.ejs')
});


app.get('/', function(req, res){
    res.render('index.ejs')
});

app.get('/transaction', function(req, res){
    res.render('card_transaction_history.ejs')
});

app.get('/recommend', function(req, res){
    res.render('recommend.ejs')
});

app.get('/grade', function(req, res){
    res.render('grade.ejs')
});

app.get('/contact', function(req, res){
    res.render('contact.ejs')
});

app.get('/login', function(req, res){
    res.render('login.ejs')
});

app.get('/register', function(req, res){
    res.render('register.ejs')
});
app.get('/translogin', function(req, res){
    res.render('translogin.ejs')
});
app.get('/recommendlogin', function(req, res){
    res.render('recommendlogin.ejs')
});


app.post('/contactProc', (req, res) => {
    const name = req.body.name;
    const email = req.body.email;
    const content = req.body.content;

    var sql = `insert into contact(name,email, content, regdate)
    values(?,?,?,now() )`
    
    var values = [name,email, content];

    connection.query(sql, values, function(err, result){
        if(err) throw err;
        console.log('자료 1개를 삽입하였습니다.');
        res.send("<script> alert('문의사항이 등록되었습니다.'); location.href='/'</script>");
    })


});

app.post('/loginProc', (req, res) => {
    // const name = req.body.name;
    // const user_id = req.body.user_id;
    const email = req.body.email;
    const pw = req.body.pw;
    // const age = req.body.age;

    var sql = `select * from user where email=? and pw=?`
    
    var values = [email,pw];

    connection.query(sql, values, function(err, result){
        if(err) throw err;

        if(result.length==0){
            res.send("<script> alert('존재하지 않는 이메일이거나 비밀번호가 틀렸습니다.'); location.href='/login'</script>");
        } else{
            console.log(result[0]);

            req.session.member = result[0]

            res.send("<script> alert('로그인 되었습니다.'); location.href='/'</script>");
            //res.send(result);
        }
    })


});

app.post('/transloginProc', (req, res) => {
    // const name = req.body.name;
    // const user_id = req.body.user_id;
    const email = req.body.email;
    const pw = req.body.pw;
    // const age = req.body.age;

    var sql = `select * from user where email=? and pw=?`
    
    var values = [email,pw];

    connection.query(sql, values, function(err, result){
        if(err) throw err;

        if(result.length==0){
            res.send("<script> alert('존재하지 않는 이메일이거나 비밀번호가 틀렸습니다.'); location.href='/login'</script>");
        } else{
            console.log(result[0]);

            req.session.member = result[0]

            res.send("<script> alert('로그인 되었습니다.'); location.href='/transaction'</script>");
            //res.send(result);
        }
    })


});

app.post('/recommendloginProc', (req, res) => {
    // const name = req.body.name;
    // const user_id = req.body.user_id;
    const email = req.body.email;
    const pw = req.body.pw;
    // const age = req.body.age;

    var sql = `select * from user where email=? and pw=?`
    
    var values = [email,pw];

    connection.query(sql, values, function(err, result){
        if(err) throw err;

        if(result.length==0){
            res.send("<script> alert('존재하지 않는 이메일이거나 비밀번호가 틀렸습니다.'); location.href='/login'</script>");
        } else{
            console.log(result[0]);

            req.session.member = result[0]

            res.send("<script> alert('로그인 되었습니다.'); location.href='/recommend'</script>");
            //res.send(result);
        }
    })


});


app.get('/logout', (req, res) => {
    
    req.session.member = null;
    res.send("<script> alert('로그아웃 되었습니다.'); location.href='/'</script>");


});

app.post('/registerProc', (req, res) => {
    const name = req.body.name;
    const user_id = req.body.user_id;
    const email = req.body.email;
    const pw = req.body.pw;
    const age = req.body.age;

    var sql = `select * from user where email=?`
    
    var sql2 = `insert into user(name,user_id, email, pw,age)values(?,?,?,?,?)`
    
    var values1 = [email]
    var values = [name,user_id,email,pw,age];

    connection.query(sql, values1, function(err, result){
        if(err) throw err;
            // console.log(result[0])
            // console.log(err)
            console.log(values)
            console.log(result)
            
        if(result.length==0){
            console.log('회원가입 성공');
            connection.query(sql2,values,function(err, result){
                res.send("<script> alert('정상적으로 회원가입 되었습니다.'); location.href='/login'</script>");
            })
            
        }else if(email==result[0].email) {
            res.send("<script> alert('이미 가입된 이메일입니다.'); location.href='/login'</script>");
        }
    })


});

app.post('/transactionProc', (req, res) => {
    const thismonth = req.body.thismonth;
    const lastmonth = req.body.lastmonth;
    const category = req.body.category;

    var sql = `insert into transaction(category, thismonth, lastmonth, regdate)
    values('${category}','${thismonth}','${lastmonth}',now() )`
    
    connection.query(sql, function(err, result){
        if(err) throw err;
        console.log('자료 1개를 삽입하였습니다.');
        res.send("<script> alert('정보가 등록되었습니다.'); location.href='/transaction'</script>");
    })


});

app.get('/contactDelete', function(req, res){
    var idx = req.query.idx
    var sql = `delete from contact where idx='${idx}'`
    connection.query(sql, function(err, result){
        if(err) throw err;
        res.send("<script> alert('삭제 되었습니다.'); location.href='/contactList'</script>");
    })
});

app.get('/contactList', (req,res)=>{

    var sql = `select * from contact order by idx desc`
    connection.query(sql,function(err,results,fields){
        if(err)throw err;
        res.render('contactList.ejs',{lists:results})
    })
})