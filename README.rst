Automatic Speech Recognition
============================

`VK speech recognition service <https://vk.com/voice-tech>`_

Allows you to convert an audio recording into a text transcript. The service uses ASR (Automatic Speech Recognition), a neural network-based speech recognition technology that reads the voice and translates it into text. This technology is used by VK to decrypt voice messages, generate subtitles in videos and much more.

Installing
----------

**Python 3.11 or higher is required**

* Clone repository into your project

.. code:: sh

    git clone https://github.com/cekmop-npu3/SpeechRecognition.git

* Create virtual environment and activate it

.. code:: sh

    python -m venv venv
    # activate in powershell
    venv\Scripts\activate.ps1
    # activate in cmd
    venv\Scripts\activate.bat

* Install required libraries

.. code:: sh

    pip install -r requirements.txt


Usage
-------------

.. code:: py

    from ASR import Asr
    from ASR.types import Text
    from asyncio import run


    async def main() -> Text:
        asr = Asr()
        return await asr.recognize('test.mp3', 'neutral')


    if __name__ == '__main__':
        run(main())