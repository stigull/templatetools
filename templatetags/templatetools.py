#coding: utf-8

from datetime import date, datetime, timedelta
from roman import toRoman

from django.conf import settings
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from utils.dateformatting import NEFNIFALL, THOLFALL, THAGUFALL, EIGNARFALL, MONTHS
from utils.dateformatting import get_day_of_week_in_icelandic

register = template.Library()

def format_datetime(dt, now_date = None):
    """
    Usage:  {{ datetime|format_datetime }}
    """
    date_verbose = u"%s, kl. %s" % (format_date(dt, THOLFALL), dt.strftime('%H:%M'))

    if now_date is None:
        now_date = datetime.now().date()
    current_date = dt.date()
    date_difference = current_date - now_date

    if current_date == now_date:
        return u"Í dag, %s" % date_verbose
    elif date_difference == timedelta(-1):
        return u"Í gær, %s" % date_verbose
    elif date_difference == timedelta(1):
        return u"Á morgun, %s" % date_verbose
    else:
        return date_verbose.capitalize()
register.filter(u'format_datetime', format_datetime)

def readable_nr_of_comments(nr_of_comments):
    """
    Usage:  {{ nr_of_comments|readable_nr_of_comments }}
    """
    if nr_of_comments < 0:
        return u""
    elif nr_of_comments == 0:
        return u"Engin athugasemd"
    elif nr_of_comments == 1:
        return u"Ein athugasemd"
    else:
        return u"%d athugasemdir" % nr_of_comments
register.filter(u'readable_nr_of_comments', readable_nr_of_comments)

def format_phone(phonenumber, language_code = 'is'):
    """
    Usage:  {{ phonenumber|format_phone:"language_code" }}
    Before: language_code is a valid language code
    After:  phonenumber has been formatted accordingly to language_code
    """
    if language_code == u"is":
        if len(phonenumber) == 7:
            return u"%s-%s" % (phonenumber[0:3], phonenumber[3:7])
        else:
            return phonenumber
    else:
        return phonenumber
register.filter(u'format_phone', format_phone)

def format_age(age_information):
    """
    Usage:  {{ age_information|format_age }}
    Before: age_information is a triplet (years, months, days)
    After:  age_information has been turned into a human readable localized string
    """
    years, months, days = age_information
    years_string, months_string, days_string = None, None, None
    if years % 10 == 1 and years != 11:
        years_string = _(u"%(years)d árs")
    else:
        years_string = _(u"%(years)d ára")
    years_string = years_string % {'years' : years }

    if months != 0:
        months_string = _(u"%(months)d mánaða") % {'months' : months }

    if days != 0:
        days_string = ungettext("%(days)d dags", "%(days)d daga", days) % {'days': days }

    #TODO: We are assuming that age is > 0 and therefore age_string is not None
    if months_string is not None and days_string is not None:
        age_string = _(u"%(years)s, %(months)s og %(days)s")
    elif months_string is None and days_string is not None:
        age_string = _(u"%(years)s og %(days)s")
    elif months_string is not None and days_string is None:
         age_string = _(u"%(years)s og %(months)s")
    else:
        return years_string

    return age_string % {'years': years_string, 'months': months_string, 'days': days_string }
register.filter(u'format_age', format_age)

ENDINGS = {}
ENDINGS[NEFNIFALL] = u"inn"
ENDINGS[THOLFALL] = u"inn"
ENDINGS[THAGUFALL] = u"num"
ENDINGS[EIGNARFALL] = u"ins"

def format_date(date, tense = NEFNIFALL):
    """
    Usage:  {% date|format_date:"beyging" %}
    Before: tense is recognized by 'nf|þf|þgf|ef'
    After:
    """
    return _(u"%(weekday_name)s%(ending)s %(day)s. %(month)s %(year)s") % {
                    'weekday_name': get_day_of_week_in_icelandic(date.weekday(), tense),
                    'ending': ENDINGS[tense],
                    'day': date.day,
                    'month': MONTHS[date.month],
                    'year': date.year }
register.filter(u'format_date', format_date)


def format_time_to_date(info):
    """
    Usage:  {{ info|format_time_to_date}}
    Before: info == (future, months, days, prefix)
    After:
    """
    has_passed, months, days, prefix = info
    info = ''
    if months == 0 and days == 0:
        return _(u"%s í dag") % prefix

    if not has_passed:
        if months == 0:
            #In this month
            if days is 1:
                info = _(u"á morgun")
            else:
                info = _(u"eftir %d daga") % days
        elif months == 1:
            #Next month
            if days == 0:
                info = _(u"eftir nákvæmlega mánuð")
            elif days == 1:
                info = _(u"eftir mánuð og einn dag")
            else:
                info = _(u"eftir mánuð og %d daga") % days
        else:
            if days == 0:
                info = _(u"eftir nákvæmlega %d mánuði") % months
            elif days == 1:
                info = _(u"eftir nákvæmlega %d mánuði og einn dag") % months
            elif days == 21 or days == 31:
                info = _(u"eftir nákvæmlega %d mánuði og %d dag") % (months, days)
            else:
                info = _(u"eftir nákvæmlega %d mánuði og %d daga") %(months, days)
    else:
        if months == 0:
            if days == 1:
                info = _(u"í gær")
            elif days == 21 or days == 31:
                info = _(u"fyrir %d degi") % days
            else:
                info = _(u"fyrir %d dögum") % days
        elif months == 1:
            if days == 0:
                info = _(u"fyrir nákvæmlega einum mánuði")
            elif days == 1:
                info = _(u"fyrir nákvæmlega einum mánuði og einum degi")
            elif days == 21 or days == 31:
                info = _(u"fyrir nákvæmlega einum mánuði og %d degi") % days
            else:
               info = _(u"fyrir nákvæmlega einum mánuði og %d dögum") % days
        else:
            if days == 0:
               info = _(u"fyrir %d mánuðum") % months
            elif days == 1:
                info = _(u"fyrir %d mánuðum og einum degi") % months
            elif days == 21 or days == 31:
                info = _(u"fyrir %d mánuðum og %d degi") % (months, days)
            else:
                info = _(u"fyrir %d mánuðum og %d dögum") %(months, days)
    return "%s %s" % (prefix, info)
register.filter("format_time_to_date", format_time_to_date)

def copyright():
    """
    Usage:  {% copyright %}
    Post:   copyright == 'settings.CREATED_YEAR' if the current year is settings.CREATED_YEAR
            else copyright == 'settings.CREATED_YEAR-YYYY' where YYYY is the current year
    """
    try:
        birthyear = settings.CREATED_YEAR
    except AttributeError, e:
        return date.today().year
    else:
        if birthyear != date.today().year:
            return  "%s - %s" % (birthyear, date.today().year)
        else:
            return birthyear
copyright = register.simple_tag(copyright)

def conditional_href(context, title, url_name):
    """
    Usage:  {% conditional_href title url_name %}
    Before: url_name is the name of a named url pattern
    After:  If request.path equals the url that url_name refers then title is not wrapped in
            an anchor element
            else it is wrapped in an anchor element
    """
    try:
        url = reverse(url_name)
        request = context['request']
    except (NoReverseMatch, KeyError), e:
        return {}

    attrs = {'title' : title, 'href' : url, 'is_href' : True }
    if request.path == url:
        attrs['is_href'] = False
    return attrs
register.inclusion_tag('snippets/conditional_href.html', takes_context = True)(conditional_href)

def get_list_of_objects(parser, token):
    """
    Usage:  {% get_list_of_objects appname modelname managername as varname %}
    After:  varname contains appname.models.modelname.managername.all()
    """
    bits = token.contents.split()
    if len(bits) != 6 and len(bits) != 5:
        raise template.TemplateSyntaxError("%s tag takes three or four arguments" % bits[0])

    if 'as' not in [bits[4],bits[3]]:
       raise template.TemplateSyntaxError("Third or fourth argument for %s must be 'as'" % bits[0])

    if len(bits) == 6:
        return GetListOfObjectsNode(bits[1], bits[2], bits[5], bits[3])
    else:
        return GetListOfObjectsNode(bits[1], bits[2], bits[4])

class GetListOfObjectsNode(template.Node):
    def __init__(self, appname, modelname, varname, managername = 'objects'):
        self.varname = varname
        self.managername = managername
        try:
            app = __import__(appname)
        except ImportError:
            raise template.TemplateSyntaxError("No application with name '%s'" % appname)
        try:
            self.model_class = getattr(app.models, modelname)
        except AttributeError:
            raise template.TemplateSyntaxError("No model with name '%s' in '%s'.models" % (modelname, appname))

    def render(self, context):
        context[self.varname] = getattr(self.model_class, self.managername).all()
        return ''
register.tag('get_list_of_objects', get_list_of_objects)

def romanize_filter(value, to_upper=True):
    """
    Change int or long into Roman Numeral

    Usage: {{ object.id|romanize:to_upper }}
    After:  integer turned to roman numeral
    """
    if isinstance(value, int) or isinstance(value, long):
        if to_upper:
            return toRoman(value)
        else:
            return toRoman(value).lower()
    else:
        return value
register.filter('romanize', romanize_filter)

def get_position_class(forloop):
    """
    Usage:  {{ forloop|get_position_class }}
    Pre:    forloop has the keys first and last
    Post:   first if and only if forloop.first is True
            last if and only if forloop.last is True
    """
    if forloop['first']:
        return u'first'
    elif forloop['last']:
        return u'last'
    else:
        return u""
register.filter("get_position_class", get_position_class)