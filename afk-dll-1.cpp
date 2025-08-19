#include "pch.h"
#include <windows.h>
#include <winternl.h>
#include <string>

#pragma comment(lib, "ntdll.lib")

typedef NTSTATUS(WINAPI* _NtQueryInformationProcess)(
    HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG
    );

typedef struct _UNICODE_STRING2 {
    USHORT Length;
    USHORT MaximumLength;
    PWSTR Buffer;
} UNICODE_STRING2, * PUNICODE_STRING2;

typedef struct _RTL_USER_PROCESS_PARAMETERS2 {
    BYTE Reserved1[16];
    PVOID Reserved2[10];
    UNICODE_STRING2 ImagePathName;
    UNICODE_STRING2 CommandLine;
} RTL_USER_PROCESS_PARAMETERS2, * PRTL_USER_PROCESS_PARAMETERS2;

typedef struct _PEB2 {
    BYTE Reserved1[2];
    BYTE BeingDebugged;
    BYTE Reserved2[1];
    PVOID Reserved3[2];
    PVOID Ldr;
    PRTL_USER_PROCESS_PARAMETERS2 ProcessParameters;
} PEB2, * PPEB2;

typedef struct _PROCESS_BASIC_INFORMATION2 {
    PVOID Reserved1;
    PPEB2 PebBaseAddress;
    PVOID Reserved2[2];
    ULONG_PTR UniqueProcessId;
    PVOID Reserved3;
} PROCESS_BASIC_INFORMATION2;

extern "C" __declspec(dllexport)
void RunStealth(const wchar_t* fakePath, const wchar_t* fakeCmd)
{
    _NtQueryInformationProcess NtQueryInformationProcess =
        (_NtQueryInformationProcess)GetProcAddress(GetModuleHandleW(L"ntdll.dll"), "NtQueryInformationProcess");

    if (!NtQueryInformationProcess)
        return;

    PROCESS_BASIC_INFORMATION2 pbi{};
    ULONG retLen = 0;

    if (!NT_SUCCESS(NtQueryInformationProcess(GetCurrentProcess(),
        ProcessBasicInformation, &pbi, sizeof(pbi), &retLen)))
        return;

    if (!pbi.PebBaseAddress)
        return;

    auto peb = pbi.PebBaseAddress;
    if (!peb->ProcessParameters)
        return;

    auto procParams = peb->ProcessParameters;

    // Safe replace ImagePathName
    if (procParams->ImagePathName.Buffer &&
        procParams->ImagePathName.MaximumLength >= sizeof(WCHAR))
    {
        wcsncpy_s(procParams->ImagePathName.Buffer,
            procParams->ImagePathName.MaximumLength / sizeof(WCHAR),
            fakePath, _TRUNCATE);
        procParams->ImagePathName.Length = (USHORT)(wcslen(fakePath) * sizeof(WCHAR));
    }

    // Safe replace CommandLine
    if (procParams->CommandLine.Buffer &&
        procParams->CommandLine.MaximumLength >= sizeof(WCHAR))
    {
        wcsncpy_s(procParams->CommandLine.Buffer,
            procParams->CommandLine.MaximumLength / sizeof(WCHAR),
            fakeCmd, _TRUNCATE);
        procParams->CommandLine.Length = (USHORT)(wcslen(fakeCmd) * sizeof(WCHAR));
    }
}
