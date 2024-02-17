from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, DateField,IntegerField
from wtforms.validators import DataRequired
from article_analysis import analyse
from html import escape

app=Flask(__name__)

class QueryForm(Form):
    query=StringField("Query",validators=[DataRequired()])
    from_date=DateField("From Date",default=None,validators=[])
    to_date=DateField("To Date",default=None,validators=[])
    max_pages=IntegerField(
        "Maximum Number of Pages (50 articles to a page)",
        validators=[DataRequired()],
        render_kw={
            "min":"1",
            "placeholder":"1"
        }
    )

    # def validate_from_date(form,field):
    #     if field.data==None:
    #         form.from_date=""

    # def validate_to_date(form,field):
    #     if field.data==None:
    #         form.to_date=""

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/makequery',methods=["GET","POST"])
def make_query():
    form=QueryForm(request.form)
    if request.method=="POST" and form.validate():
        query=form.query.data
        from_date=form.from_date.data
        to_date=form.to_date.data
        max_pages=form.max_pages.data

        filename=query.replace(' ','')+".csv"
        print(f"Filename {filename}")

        escaped_query=escape(query)

        print("analysis attempted")

        analyse(
            escaped_query,
            filename,
            from_date,
            to_date,
            max_pages
        )

        print("analysis done")

        return redirect(url_for('showresults'))
    
    return render_template('makequery.html',form=form)

@app.route('/showresults')
def show_query():

    return render_template('showresults.html')

@app.route('/me')
def me():
    return render_template('me.html')

if __name__=='__main__':
    app.debug=True
    app.run()