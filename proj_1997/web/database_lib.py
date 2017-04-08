from web.models import *
from django.shortcuts import get_object_or_404

def get_index_info():
    return {
        'header': index_info.objects.all()[0],
        'sliders': slider.objects.all().order_by('order')
    }


def get_teacher_of(_id):
    return get_object_or_404(teacher, id=_id)


def get_msg_settings():
    st = get_object_or_404(system_setting, id=1)
    return st.msg_account, st.msg_pwd


def set_rsv_status(_id, status):
    rsv = get_object_or_404(reservation, id=_id)
    rsv.status = status
    rsv.save()

    return True