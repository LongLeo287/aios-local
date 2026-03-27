<#
.SYNOPSIS
    AI OS Corp — Load Secrets into $env:* for current session.
    Tiện ích được gọi bởi các script khác để load secrets trước khi chạy.

.DESCRIPTION
    Dot-source file này để load toàn bộ secrets từ MASTER.env (hoặc .dpapi)
    vào môi trường của PowerShell session hiện tại.

.USAGE
    # Từ bất kỳ script nào:
    $SecretsLoader = Join-Path $AiOsRoot "ops\secrets\load-env.ps1"
    if (Test-Path $SecretsLoader) { . $SecretsLoader }

    # Sau đó dùng trực tiếp:
    $env:TELEGRAM_BOT_TOKEN
    $env:OPENAI_API_KEY
    # ...etc
#>

# Resolve secrets dir relative to THIS file
$_SecretsDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Silently delegate to decrypt.ps1
. (Join-Path $_SecretsDir "decrypt.ps1")
