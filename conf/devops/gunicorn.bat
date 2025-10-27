@rem ------------------- batch setting -------------------
@echo off

@rem ------------------- declare variable -------------------
if not defined PROJECT_ENV (set PROJECT_ENV=cli)

@rem ------------------- execute script -------------------
call :%*
goto end

@rem ------------------- declare function -------------------

:action-prepare
    echo ^> Startup and into container for develop algorithm
    @rem build image
    if NOT EXIST %cd%\conf\docker\%VAR_SRV_HOSTNAME%\server (mkdir %cd%\conf\docker\%VAR_SRV_HOSTNAME%\server)
    if NOT EXIST %cd%\conf\docker\isa\api (mkdir %cd%\conf\docker\isa\api)
    if NOT EXIST %cd%\conf\docker\isa\cli (mkdir %cd%\conf\docker\isa\cli)
    if NOT EXIST %cd%\conf\docker\isa\modules (mkdir %cd%\conf\docker\isa\modules)
    if NOT EXIST %cd%\conf\docker\isa\configs (mkdir %cd%\conf\docker\isa\configs)
    xcopy /Y %cd%\app\api\docker-entrypoint.sh %cd%\conf\docker\isa\api\docker-entrypoint.sh
    docker build -t %ISA_DOCKER_IMAGE% ./conf/docker/isa
    docker build -t %INFRA_DOCKER_IMAGE% ./conf/docker/%VAR_SRV_HOSTNAME%
    docker build -t %TESTER_DOCKER_IMAGE% ./conf/docker/tester

    echo ^> Build virtual network
    set network_exist=1
    for /f "tokens=1" %%p in ('docker network ls --filter "name=%INFRA_DOCKER_NETWORK%" --format "{{.ID}}"') do (set network_exist=)
    if defined network_exist (docker network create %INFRA_DOCKER_NETWORK%)
    goto end

:action
    @rem declare variable
    set VAR_SRV_PORT=8082
    set VAR_SRV_HOSTNAME=gunicorn
    set DOCKER_CONTAINER_NAME=%VAR_SRV_HOSTNAME%-%PROJECT_NAME%
    set ISA_DOCKER_IMAGE=isa:%PROJECT_NAME%
    set TESTER_DOCKER_IMAGE=tester:%PROJECT_NAME%
    set INFRA_DOCKER_IMAGE=%VAR_SRV_HOSTNAME%:%PROJECT_NAME%
    set INFRA_DOCKER_NETWORK=benchmark-network
    set DC_ENV=%CLI_DIRECTORY%\cache\docker-compose-%VAR_SRV_HOSTNAME%.env
    set DC_CONF=%CLI_DIRECTORY%\conf\docker\docker-compose-%VAR_SRV_HOSTNAME%.yml

    @rem management container
    if defined TARGET_PROJECT_STOP (
        echo Stop project %PROJECT_NAME% develop server
        docker compose --file !DC_CONF! --env-file !DC_ENV! down
    ) else (
        echo Start project %PROJECT_NAME% develop server
        if "%TARGET_PROJECT_COMMAND%"=="bash" (
            if NOT DEFINED TARGET_CONTAINER_NAME (
                echo ^> Into service '%DOCKER_CONTAINER_NAME%'
                docker exec -ti %DOCKER_CONTAINER_NAME% bash
            ) else (
                echo ^> Into service '%DOCKER_CONTAINER_NAME%_%TARGET_CONTAINER_NAME%'
                docker exec -ti %DOCKER_CONTAINER_NAME%_%TARGET_CONTAINER_NAME% bash
            )
        ) else (
            echo ^> Startup service
            call :action-prepare

            @rem execute container
            echo ^> Start container with docker-compose
            IF EXIST !DC_CONF! (
                @rem create docker-compose env file
                IF EXIST !DC_ENV! (del !DC_ENV!)
                echo PROJECT_NAME=%PROJECT_NAME% > !DC_ENV!
                echo PROJECT_DIR=%CLI_DIRECTORY% >> !DC_ENV!
                echo SRV_HOSTNAME=%VAR_SRV_HOSTNAME% >> !DC_ENV!
                echo SRV_ISA_IMAGE_NAME=%ISA_DOCKER_IMAGE%  >> !DC_ENV!
                echo SRV_INFRA_IMAGE_NAME=%INFRA_DOCKER_IMAGE%  >> !DC_ENV!
                echo SRV_TESTER_IMAGE_NAME=%TESTER_DOCKER_IMAGE%  >> !DC_ENV!
                echo SRV_CONTAINER_NAME=%DOCKER_CONTAINER_NAME% >> !DC_ENV!
                echo SRV_PORT=%VAR_SRV_PORT% >> !DC_ENV!
                echo INFRA_DOCKER_NETWORK=%INFRA_DOCKER_NETWORK% >> !DC_ENV!

                @rem startup with docker-compose
                docker compose --file !DC_CONF! --env-file !DC_ENV! up -d
            )
        )
    )
    goto end

:args
    set COMMON_ARGS_KEY=%1
    set COMMON_ARGS_VALUE=%2
    if "%COMMON_ARGS_KEY%"=="--stop" (set TARGET_PROJECT_STOP=true)
    if "%COMMON_ARGS_KEY%"=="--into" (
        set TARGET_PROJECT_COMMAND=bash
        if DEFINED COMMON_ARGS_VALUE (
            set TARGET_CONTAINER_NAME=%COMMON_ARGS_VALUE%
        )
    )
    goto end

:short
    echo Gunicorn ( Single-worker ) + Flask
    goto end

:help
    echo This is a Command Line Interface with project %PROJECT_NAME%
    echo Gunicorn ( Single-worker ) + Flask benchmark.
    echo.
    echo Options:
    echo      --help, -h        Show more information with '%~n0' command.
    echo      --into            Into container when it is at detach mode.
    echo      --stop            Stop container if dev-server was on work.
    call %CLI_SHELL_DIRECTORY%\utils\tools.bat command-description %~n0
    goto end

:end
