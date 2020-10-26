@ECHO OFF
IF EXIST venv (
    "venv/scripts/activate"
) else (
    if [%1]==[c] (
        ECHO creating vertual env
        if NOT [%2]==[] (
            python -m venv %2
            ECHO vertual env created [%2]
        ) else (
            python -m venv venv
            ECHO vertual env created [venv]
        )
        "venv/scripts/activate"
    ) else (
        ECHO no vertual env in this directory
    )
)