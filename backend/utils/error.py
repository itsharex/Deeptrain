from django.shortcuts import render


def throw_bad_request(request, reason):
    return render(request, "error.html", {"reason": reason})
