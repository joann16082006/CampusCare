from .models import Grievance, GrievanceHistory


def notifications(request):
    """Adds popup data to every page."""
    if not request.user.is_authenticated:
        return {}

    try:
        role = request.user.profile.role
    except Exception:
        return {}

    # Staff: how many grievances they have not seen yet
    if role in ('STAFF', 'ADMIN'):
        return {
            'new_grievance_count': Grievance.objects.filter(staff_seen=False).count(),
        }

    # Student: status changes they have not been told about yet
    if role == 'STUDENT':
        updates = list(
            GrievanceHistory.objects
            .filter(grievance__student=request.user, student_notified=False)
            .select_related('grievance')
            .order_by('changed_at')
        )
        if updates:
            # Mark them as shown, so each popup appears only once
            GrievanceHistory.objects.filter(
                pk__in=[u.pk for u in updates]
            ).update(student_notified=True)
        return {'status_updates': updates}

    return {}