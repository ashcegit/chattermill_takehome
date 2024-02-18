from flask import Flask,render_template,request,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, DateField,IntegerField
from wtforms.validators import DataRequired
from article_analysis import analyse
from html import escape
from datetime import datetime
import os

app=Flask(__name__)

class NullableDateField(DateField):
    """
    Nullable version of native WTForms DateField Class
    """

    def process_formdata(self,values):
        if values:
            date_string=' '.join(values).strip()
            if date_string=='':
                self.data=None
                return
            
            try:
                self.data=datetime.strptime(date_string,self.format).date()
            except ValueError:
                self.data=None
                raise ValueError(self.gettext('Not a valid date value'))

class QueryForm(Form):
    query=StringField("Query",validators=[DataRequired()])
    from_date=NullableDateField("From Date",default=None,validators=[])
    to_date=NullableDateField("To Date",default=None,validators=[])
    max_pages=IntegerField(
        "Maximum Number of Pages (50 articles to a page)",
        validators=[DataRequired()],
        default="1",
        render_kw={
            "min":"1",
        }
    )

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')    

@app.route('/makequery',methods=["GET","POST"])
def make_query():
    form=QueryForm(request.form)
    if request.method=="POST" and form.validate():
        succeeded=False
        query=form.query.data
        from_date=form.from_date.data
        to_date=form.to_date.data
        max_pages=form.max_pages.data

        filename="reports/{}{}{}_{}_max_pages".format(
            query.replace(' ',''),
            "_from{}".format(str(from_date)) if from_date!=None else "",
            "_to{}".format(str(to_date)) if to_date!=None else "",
            max_pages)+".csv"
        
        #check if file already exists - if so, skip

        if os.path.exists(filename):
            succeeded=True
        else:
            escaped_query=escape(query)

            succeeded=analyse(
                escaped_query,
                filename,
                from_date,
                to_date,
                max_pages
            )

        if(succeeded):
            session['filename']=filename
            return redirect(url_for('show_results'))
        else:
            return redirect(url_for('query_failed'))
        
    return render_template('makequery.html',form=form,submitted=False)

@app.route('/showresults')
def show_results():
    filename=session['filename']
    session.clear()

    

    return render_template('showresults.html')

@app.route('/queryfailed')
def query_failed():

    return render_template('queryfailed.html')

@app.route('/me')
def me():
    return render_template('me.html')

if __name__=='__main__':
    app.secret_key='c3VwZXIgZHVwZXIgc2VjcmV0IGtleQ=='
    app.config['SESSION_TYPE']='filesystem'
    app.debug=True
    app.run()