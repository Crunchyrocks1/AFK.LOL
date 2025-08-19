


#include "pch.h"
#include <windows.h>

static HMODULE g_hModule = nullptr;

// Store a reference to our own DLL when loaded
extern "C" BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID /*lpReserved*/)
{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        g_hModule = hModule;
        DisableThreadLibraryCalls(hModule);
    }
    return TRUE;
}

// Read this DLL's bytes into a memory buffer allocated with HeapAlloc
// Caller must free with FreeSelfMemory()
extern "C" __declspec(dllexport)
BOOL ReadSelfToMemory(BYTE** outData, DWORD* outSize)
{
    if (!outData || !outSize) return FALSE;
    *outData = nullptr;
    *outSize = 0;

    // Get path to this DLL on disk
    wchar_t path[MAX_PATH];
    DWORD len = GetModuleFileNameW(g_hModule, path, MAX_PATH);
    if (len == 0 || len >= MAX_PATH) return FALSE;

    // Open DLL file
    HANDLE hFile = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, nullptr,
        OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
    if (hFile == INVALID_HANDLE_VALUE) return FALSE;

    // Get file size
    LARGE_INTEGER liSize{};
    if (!GetFileSizeEx(hFile, &liSize) || liSize.QuadPart > 0xFFFFFFFF) {
        CloseHandle(hFile);
        return FALSE;
    }
    DWORD size = static_cast<DWORD>(liSize.QuadPart);

    // Allocate buffer
    BYTE* buf = static_cast<BYTE*>(HeapAlloc(GetProcessHeap(), 0, size));
    if (!buf) {
        CloseHandle(hFile);
        return FALSE;
    }

    // Read file into buffer
    DWORD bytesRead = 0;
    BOOL ok = ReadFile(hFile, buf, size, &bytesRead, nullptr);
    CloseHandle(hFile);

    if (!ok || bytesRead != size) {
        HeapFree(GetProcessHeap(), 0, buf);
        return FALSE;
    }

    *outData = buf;
    *outSize = size;
    return TRUE;
}

// Free memory previously allocated by ReadSelfToMemory
extern "C" __declspec(dllexport)
void FreeSelfMemory(BYTE* ptr)
{
    if (ptr) {
        HeapFree(GetProcessHeap(), 0, ptr);
    }
}
