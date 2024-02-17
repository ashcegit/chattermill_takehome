from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, DateField,IntegerField
from wtforms.validators import DataRequired
from article_analysis import analyse
from html import escape
from datetime import datetime

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

        escaped_query=escape(query)

        print(from_date)
        print(to_date)

        print("analysis attempted")

        analyse(
            escaped_query,
            filename,
            from_date,
            to_date,
            max_pages
        )

        print("analysis done")

        return redirect(url_for('show_results'))
    
    return render_template('makequery.html',form=form)

@app.route('/showresults')
def show_results():

    return render_template('showresults.html')

@app.route('/me')
def me():
    return render_template('me.html')

if __name__=='__main__':
    app.debug=True
    app.run()