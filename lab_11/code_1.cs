using System;

class Program
{
    static void Main()
    {
        string plaintext = "Муха Богдан";
        string key = GenerateRandomKey(plaintext.Length);

        Console.WriteLine($"Текст для шифрування: {plaintext}");
        Console.WriteLine();
        Console.WriteLine($"Випадковий ключ: {key}");

        string ciphertext = Encrypt(plaintext, key);
        Console.WriteLine($"Зашифрований текст: {ciphertext}");

        string decryptedText = Decrypt(ciphertext, key);
        Console.WriteLine();
        Console.WriteLine($"Розшифрований текст: {decryptedText}");
        Console.WriteLine();
    }

    static string Encrypt(string plaintext, string key)
    {
        char[] result = new char[plaintext.Length];
        for (int i = 0; i < plaintext.Length; i++)
        {
            if (plaintext[i] == ' ')
            {
                result[i] = ' ';
                continue;
            }
            result[i] = ShiftChar(plaintext[i], key[i]);
        }
        return new string(result);
    }

    static string Decrypt(string ciphertext, string key)
    {
        char[] result = new char[ciphertext.Length];
        for (int i = 0; i < ciphertext.Length; i++)
        {
            if (ciphertext[i] == ' ')
            {
                result[i] = ' ';
                continue;
            }
            result[i] = ShiftChar(ciphertext[i], key[i], true); 
        }
        return new string(result);
    }

    static char ShiftChar(char ch, char keyChar, bool decrypt = false)
    {
        string alphabet = "АБВГҐДЕЄЖЗИЙІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ ";
        int alphabetLength = alphabet.Length;

        int chIndex = alphabet.IndexOf(ch);
        int keyIndex = alphabet.IndexOf(keyChar);

        if (chIndex < 0 || keyIndex < 0) return ch;

        int shiftedIndex = decrypt ? (chIndex - keyIndex + alphabetLength) % alphabetLength : (chIndex + keyIndex) % alphabetLength;
        return alphabet[shiftedIndex];
    }

    static string GenerateRandomKey(int length)
    {
        Random random = new Random();
        string alphabet = "АБВГҐДЕЄЖЗИЙІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ ";
        char[] key = new char[length];

        for (int i = 0; i < length; i++)
        {
            key[i] = alphabet[random.Next(alphabet.Length)];
        }

        return new string(key);
    }
